"""Authentication utility module for AWS Cognito integration.

This module provides the Auth class that handles retrieval of Cognito
configuration from AWS Secrets Manager and initializes the Cognito
authenticator used to protect the Streamlit application with user login.
"""

import boto3
import json
from streamlit_cognito_auth import CognitoAuthenticator


class Auth:
    """Authentication helper for integrating Streamlit with AWS Cognito.

    This class provides static methods to set up Cognito-based authentication
    by retrieving secrets from AWS Secrets Manager and constructing the
    appropriate authenticator instance.
    """

    @staticmethod
    def get_authenticator(secret_id, region):
        """Retrieve Cognito parameters from Secrets Manager and create an authenticator.

        Fetches the Cognito User Pool ID, App Client ID, and App Client Secret
        from an AWS Secrets Manager secret, then constructs and returns a
        CognitoAuthenticator instance that can be used to gate access to
        Streamlit pages.

        Args:
            secret_id: The name or ARN of the Secrets Manager secret containing
                Cognito configuration parameters (pool_id, app_client_id,
                app_client_secret).
            region: The AWS region where the Secrets Manager secret is stored.

        Returns:
            A CognitoAuthenticator instance configured with the retrieved
            Cognito parameters.

        Raises:
            botocore.exceptions.ClientError: If the secret cannot be retrieved
                from Secrets Manager.
        """
        # Create Secrets Manager client for the specified region
        secretsmanager_client = boto3.client(
            "secretsmanager",
            region_name=region
        )

        # Retrieve the secret value containing Cognito configuration
        response = secretsmanager_client.get_secret_value(
            SecretId=secret_id,
        )

        # Parse the JSON secret string to extract individual parameters
        secret_string = json.loads(response['SecretString'])
        pool_id = secret_string['pool_id']
        app_client_id = secret_string['app_client_id']
        app_client_secret = secret_string['app_client_secret']

        # Initialize and return the CognitoAuthenticator with extracted credentials
        authenticator = CognitoAuthenticator(
            pool_id=pool_id,
            app_client_id=app_client_id,
            app_client_secret=app_client_secret,
        )

        return authenticator
