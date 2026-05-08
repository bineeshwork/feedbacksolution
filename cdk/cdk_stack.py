"""AWS CDK stack definition for the Student Feedback infrastructure.

This module defines the CdkStack class that provisions all AWS resources
required to run the Student Feedback Streamlit application, including:
- Amazon Cognito for user authentication
- AWS Secrets Manager for storing Cognito parameters
- VPC networking with public and private subnets
- ECS Fargate service running the Streamlit Docker container
- Application Load Balancer for traffic routing
- CloudFront distribution for HTTPS termination and caching
- IAM policies for Bedrock and Secrets Manager access
"""

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_cognito as cognito,
    aws_secretsmanager as secretsmanager,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_elasticloadbalancingv2 as elbv2,
    SecretValue,
    CfnOutput,
)
from constructs import Construct
from docker_app.config_file import Config

# Custom HTTP header name used to restrict ALB access to CloudFront only
CUSTOM_HEADER_NAME = "X-Custom-Header"


class CdkStack(Stack):
    """AWS CDK stack for the Student Feedback application infrastructure.

    This stack creates a fully managed, serverless web application architecture
    using ECS Fargate behind CloudFront, with Cognito authentication and
    Bedrock AI integration. The architecture ensures that the ALB only accepts
    traffic from CloudFront by validating a custom header on each request.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Initialize the CDK stack and provision all AWS resources.

        Args:
            scope: The parent construct (typically the CDK App).
            construct_id: A unique identifier for this stack within the scope.
            **kwargs: Additional stack properties such as env, description, etc.
        """
        super().__init__(scope, construct_id, **kwargs)

        # Define prefix that will be used in some resource names
        prefix = Config.STACK_NAME

        # --- Authentication Layer ---
        # Create Cognito user pool for managing application users
        user_pool = cognito.UserPool(self, f"{prefix}UserPool")

        # Create Cognito app client with a generated secret for server-side auth
        user_pool_client = cognito.UserPoolClient(self, f"{prefix}UserPoolClient",
                                                  user_pool=user_pool,
                                                  generate_secret=True
                                                  )

        # Store Cognito parameters in Secrets Manager so the ECS container
        # can retrieve them at runtime without hardcoding credentials
        secret = secretsmanager.Secret(self, f"{prefix}ParamCognitoSecret",
                                       secret_object_value={
                                           "pool_id": SecretValue.unsafe_plain_text(user_pool.user_pool_id),
                                           "app_client_id": SecretValue.unsafe_plain_text(user_pool_client.user_pool_client_id),
                                           "app_client_secret": user_pool_client.user_pool_client_secret
                                       },
                                       # This secret name should be identical
                                       # to the one defined in the Streamlit
                                       # container
                                       secret_name=Config.SECRETS_MANAGER_ID
                                       )

        # --- Networking Layer ---
        # Create a VPC with public and private subnets across 2 AZs
        vpc = ec2.Vpc(
            self,
            f"{prefix}AppVpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            vpc_name=f"{prefix}-stl-vpc",
            nat_gateways=1,
        )

        # Security group for ECS tasks - only accepts traffic from the ALB
        ecs_security_group = ec2.SecurityGroup(
            self,
            f"{prefix}SecurityGroupECS",
            vpc=vpc,
            security_group_name=f"{prefix}-stl-ecs-sg",
        )

        # Security group for the Application Load Balancer
        alb_security_group = ec2.SecurityGroup(
            self,
            f"{prefix}SecurityGroupALB",
            vpc=vpc,
            security_group_name=f"{prefix}-stl-alb-sg",
        )

        # Allow inbound traffic from ALB to ECS on the Streamlit port (8501)
        ecs_security_group.add_ingress_rule(
            peer=alb_security_group,
            connection=ec2.Port.tcp(8501),
            description="ALB traffic",
        )

        # --- Compute Layer ---
        # Create ECS cluster with Fargate capacity provider
        cluster = ecs.Cluster(
            self,
            f"{prefix}Cluster",
            enable_fargate_capacity_providers=True,
            vpc=vpc)

        # Create an internet-facing ALB in public subnets to route traffic to ECS
        alb = elbv2.ApplicationLoadBalancer(
            self,
            f"{prefix}Alb",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name=f"{prefix}-stl",
            security_group=alb_security_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        # Define the Fargate task with minimal resource allocation
        fargate_task_definition = ecs.FargateTaskDefinition(
            self,
            f"{prefix}WebappTaskDef",
            memory_limit_mib=512,
            cpu=256,
        )

        # Build the Docker image from the local docker_app directory and push to ECR
        image = ecs.ContainerImage.from_asset('docker_app')

        # Add the Streamlit container to the task definition
        fargate_task_definition.add_container(
            f"{prefix}WebContainer",
            image=image,
            port_mappings=[
                ecs.PortMapping(
                    container_port=8501,
                    protocol=ecs.Protocol.TCP)],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
        )

        # Deploy the Fargate service in private subnets with NAT egress
        service = ecs.FargateService(
            self,
            f"{prefix}ECSService",
            cluster=cluster,
            task_definition=fargate_task_definition,
            service_name=f"{prefix}-stl-front",
            security_groups=[ecs_security_group],
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        )

        # --- IAM Permissions ---
        # Grant the ECS task role permission to invoke Bedrock models
        bedrock_policy = iam.Policy(self, f"{prefix}BedrockPolicy",
                                    statements=[
                                        iam.PolicyStatement(
                                            actions=["bedrock:InvokeModel"],
                                            resources=["*"]
                                        )
                                    ]
                                    )
        task_role = fargate_task_definition.task_role
        task_role.attach_inline_policy(bedrock_policy)

        # Grant the ECS task role permission to read Cognito secrets
        secret.grant_read(task_role)

        # --- Content Delivery Layer ---
        # Configure CloudFront to use ALB as origin with a custom header
        # for origin access restriction
        origin = origins.LoadBalancerV2Origin(
            alb,
            custom_headers={CUSTOM_HEADER_NAME: Config.CUSTOM_HEADER_VALUE},
            origin_shield_enabled=False,
            protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
        )

        # Create CloudFront distribution with HTTPS redirect and no caching
        # to ensure dynamic Streamlit content is always fresh
        cloudfront_distribution = cloudfront.Distribution(
            self,
            f"{prefix}CfDist",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER,
            ),
        )

        # --- ALB Listener Configuration ---
        # Add HTTP listener on port 80
        http_listener = alb.add_listener(
            f"{prefix}HttpListener",
            port=80,
            open=True,
        )

        # Route requests with the correct custom header to the ECS target group
        http_listener.add_targets(
            f"{prefix}TargetGroup",
            target_group_name=f"{prefix}-tg",
            port=8501,
            priority=1,
            conditions=[
                elbv2.ListenerCondition.http_header(
                    CUSTOM_HEADER_NAME,
                    [Config.CUSTOM_HEADER_VALUE])],
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[service],
        )

        # Add a default action to deny all requests without the custom header,
        # preventing direct access to the ALB that bypasses CloudFront
        http_listener.add_action(
            "default-action",
            action=elbv2.ListenerAction.fixed_response(
                status_code=403,
                content_type="text/plain",
                message_body="Access denied",
            ),
        )

        # --- Stack Outputs ---
        # Output the CloudFront URL for accessing the application
        CfnOutput(self, "CloudFrontDistributionURL",
                  value=cloudfront_distribution.domain_name)
        # Output the Cognito User Pool ID for user management
        CfnOutput(self, "CognitoPoolId",
                  value=user_pool.user_pool_id)
