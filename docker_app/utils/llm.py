import boto3
import json

try:
    from constants import (
        LLM_MODEL_ID,
        LLM_MAX_TOKENS,
        LLM_TEMPERATURE,
        LLM_ACCEPT_TYPE,
        LLM_CONTENT_TYPE,
    )
except ImportError:
    from docker_app.constants import (
        LLM_MODEL_ID,
        LLM_MAX_TOKENS,
        LLM_TEMPERATURE,
        LLM_ACCEPT_TYPE,
        LLM_CONTENT_TYPE,
    )


class Llm:

    def __init__(self, bedrock_region):
        # Create Bedrock client
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=bedrock_region,
        )
        self.bedrock_client = bedrock_client

    def invoke(self, input_text):
        """
        Make a call to the foundation model through Bedrock
        """

        # Prepare a Bedrock API call to invoke a foundation model
        prompt = f"""\n\nHuman: {input_text}
                    \n\nAssistant:"""

        body = {
            "prompt": prompt,
            "max_tokens_to_sample": LLM_MAX_TOKENS,
            "temperature": LLM_TEMPERATURE,
        }
        body = json.dumps(body)

        # Make the API call to Bedrock
        response = self.bedrock_client.invoke_model(
            body=body, modelId=LLM_MODEL_ID, accept=LLM_ACCEPT_TYPE, contentType=LLM_CONTENT_TYPE
        )

        return response
