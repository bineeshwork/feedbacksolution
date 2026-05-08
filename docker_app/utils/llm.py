"""Language model utility module for Amazon Bedrock integration.

This module provides the Llm class that wraps interactions with Amazon
Bedrock's foundation models, specifically Anthropic's Claude v2, to
generate AI-powered responses for the student feedback application.
"""

import boto3
import json


class Llm:
    """Wrapper class for invoking foundation models through Amazon Bedrock.

    This class manages the Bedrock runtime client and provides a simple
    interface to send prompts to Claude v2 and receive generated responses.

    Attributes:
        bedrock_client: A boto3 Bedrock runtime client configured for
            the specified AWS region.
    """

    def __init__(self, bedrock_region):
        """Initialize the Llm instance with a Bedrock runtime client.

        Args:
            bedrock_region: The AWS region where Amazon Bedrock is available
                and the foundation model should be invoked.
        """
        # Create Bedrock runtime client for model invocation
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=bedrock_region,
        )
        self.bedrock_client = bedrock_client

    def invoke(self, input_text):
        """Invoke the Claude v2 foundation model through Amazon Bedrock.

        Constructs a prompt in the Human/Assistant format required by Claude,
        sends it to the Bedrock API, and returns the raw response.

        Args:
            input_text: The user's input text to send to the model as
                the Human turn in the conversation.

        Returns:
            The raw Bedrock API response object containing the model's
            generated completion in the response body.

        Raises:
            botocore.exceptions.ClientError: If the Bedrock API call fails
                due to permissions, throttling, or service errors.
        """
        # Format the input text into Claude's expected Human/Assistant prompt structure
        prompt = f"""\n\nHuman: {input_text}
                    \n\nAssistant:"""

        # Configure model parameters for deterministic output (temperature=0)
        model_id = "anthropic.claude-v2"
        body = {
            "prompt": prompt,
            "max_tokens_to_sample": 4096,
            "temperature": 0.,
        }
        body = json.dumps(body)
        accept = 'application/json'
        contentType = 'application/json'

        # Make the API call to Bedrock to invoke the foundation model
        response = self.bedrock_client.invoke_model(
            body=body, modelId=model_id, accept=accept, contentType=contentType
        )

        return response
