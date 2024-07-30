import boto3
import argparse
from botocore.exceptions import ClientError


parser = argparse.ArgumentParser(description='Chat with a LLM')
parser.add_argument("--model",
                    default = 'meta.llama3-1-405b-instruct-v1:0',
                    help="Choose a model from https://us-east-1.console.aws.amazon.com/sagemaker/home?region=us-east-1#/foundation-models")
parser.add_argument("--region",
                    default = 'us-west-2',
                    help="AWS region name")
parser.add_argument("--message",
                    default = 'What is AWS?',
                    help="Your message or question to LLM")

args = parser.parse_args()

# create a Bedrock Runtime client in the AWS region
client = boto3.client("bedrock-runtime", region_name=args.region)

# Set the user provided model id or use default
model_id = args.model

# Start a conversation with the user message.
user_message = args.message
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)










