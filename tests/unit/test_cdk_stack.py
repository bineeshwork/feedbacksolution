import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from cdk.cdk_stack import CdkStack
from docker_app.config_file import Config


@pytest.fixture(scope="module")
def template():
    app = core.App()
    stack = CdkStack(app, "cdk")
    return assertions.Template.from_stack(stack)


def test_cognito_user_pool_created(template):
    template.resource_count_is("AWS::Cognito::UserPool", 1)


def test_cognito_user_pool_client_created(template):
    template.has_resource_properties("AWS::Cognito::UserPoolClient", {
        "GenerateSecret": True
    })


def test_secrets_manager_secret_created(template):
    template.has_resource_properties("AWS::SecretsManager::Secret", {
        "Name": Config.SECRETS_MANAGER_ID
    })


def test_vpc_created(template):
    template.has_resource_properties("AWS::EC2::VPC", {
        "CidrBlock": "10.0.0.0/16"
    })


def test_ecs_cluster_created(template):
    template.resource_count_is("AWS::ECS::Cluster", 1)


def test_ecs_fargate_service_created(template):
    template.has_resource_properties("AWS::ECS::Service", {
        "LaunchType": "FARGATE",
        "ServiceName": "StudentFeedback-stl-front"
    })


def test_fargate_task_definition_created(template):
    template.has_resource_properties("AWS::ECS::TaskDefinition", {
        "Cpu": "256",
        "Memory": "512"
    })


def test_alb_created(template):
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::LoadBalancer", {
        "Scheme": "internet-facing",
        "Name": "StudentFeedback-stl"
    })


def test_alb_listener_created(template):
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 80,
        "Protocol": "HTTP"
    })


def test_alb_listener_default_action_denies(template):
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "DefaultActions": [
            {
                "FixedResponseConfig": {
                    "StatusCode": "403"
                },
                "Type": "fixed-response"
            }
        ]
    })


def test_alb_target_group_with_custom_header(template):
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::ListenerRule", {
        "Conditions": assertions.Match.array_with([
            assertions.Match.object_like({
                "Field": "http-header",
                "HttpHeaderConfig": {
                    "HttpHeaderName": "X-Custom-Header",
                    "Values": [Config.CUSTOM_HEADER_VALUE]
                }
            })
        ])
    })


def test_cloudfront_distribution_created(template):
    template.has_resource_properties("AWS::CloudFront::Distribution", {
        "DistributionConfig": assertions.Match.object_like({
            "DefaultCacheBehavior": assertions.Match.object_like({
                "ViewerProtocolPolicy": "redirect-to-https"
            })
        })
    })


def test_ecs_security_group_created(template):
    template.has_resource_properties("AWS::EC2::SecurityGroup", {
        "GroupName": "StudentFeedback-stl-ecs-sg"
    })


def test_alb_security_group_created(template):
    template.has_resource_properties("AWS::EC2::SecurityGroup", {
        "GroupName": "StudentFeedback-stl-alb-sg"
    })


def test_bedrock_iam_policy_created(template):
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": assertions.Match.object_like({
            "Statement": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Action": "bedrock:InvokeModel",
                    "Effect": "Allow"
                })
            ])
        })
    })


def test_cloudfront_output_exists(template):
    template.has_output("CloudFrontDistributionURL", {})


def test_cognito_pool_id_output_exists(template):
    template.has_output("CognitoPoolId", {})


def test_resource_counts(template):
    template.resource_count_is("AWS::EC2::SecurityGroup", 2)
    template.resource_count_is("AWS::EC2::VPC", 1)
    template.resource_count_is("AWS::ECS::Cluster", 1)
    template.resource_count_is("AWS::CloudFront::Distribution", 1)
