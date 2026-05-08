"""Configuration module for the Student Feedback application.

This module defines the Config class that centralizes all configurable
parameters for both the CDK infrastructure stack and the Streamlit
application, including stack naming, security settings, secrets management,
and AWS region configuration.
"""


class Config:
    """Central configuration class for the Student Feedback solution.

    This class holds all static configuration values used across the CDK
    stack deployment and the Docker-based Streamlit application. Modify
    these values to customize the deployment for different environments.
    """

    # Stack name used as a prefix for all AWS resource names.
    # Change this value if you want to create a new instance of the stack.
    STACK_NAME = "StudentFeedback"

    # Custom header value used to restrict ALB access to CloudFront only.
    # This prevents direct access to the ALB, ensuring all traffic flows
    # through CloudFront. You can choose any random string.
    CUSTOM_HEADER_VALUE = "My_random_value_58dsvasdaswcd5e4s31"

    # ID of the Secrets Manager secret containing Cognito parameters.
    # When you delete a secret, you cannot create another one immediately
    # with the same name. Change this value if you destroy your stack and need
    # to recreate it with the same STACK_NAME.
    SECRETS_MANAGER_ID = f"{STACK_NAME}ParamCognitoSecret12345"

    # AWS region in which you want to deploy the CDK stack
    DEPLOYMENT_REGION = "us-east-1"

    # AWS region where Amazon Bedrock is activated.
    # If Bedrock is not activated in us-east-1 in your account, set this value
    # accordingly.
    BEDROCK_REGION = "us-east-1"
