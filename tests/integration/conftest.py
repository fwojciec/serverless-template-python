import os
import pytest
import boto3
import datetime
import subprocess


DEFAULT_NAME = "serverless-template-python"
STACK_NAME = os.getenv("STACK_NAME")
IS_USING_EPHEMERAL_STACK = STACK_NAME is None


@pytest.fixture(scope="session")
def cf_client():
    return boto3.client("cloudformation")


@pytest.fixture(scope="session")
def stack_name(cf_client):
    if IS_USING_EPHEMERAL_STACK:
        stack_name = generate_ephemeral_stack_name()
        subprocess.run(["sh", "deploy.sh", stack_name]).check_returncode()
        print(f"Using ephemeral stack {stack_name}")
        yield stack_name
        print(f"Deleting ephemeral stack {stack_name}")
        cf_client.delete_stack(StackName=stack_name)
    else:
        print(f"Using existing stack {STACK_NAME}")
        yield STACK_NAME
        print(f"Keeping existing stack {STACK_NAME}")


@pytest.fixture(scope="session")
def api_id(stack_name, cf_client):
    outs = cf_client.describe_stacks(StackName=stack_name)["Stacks"][0]["Outputs"]
    api_id = next(out["OutputValue"] for out in outs if out["OutputKey"] == "HttpApi")
    print(f"Using API [{api_id}]")
    return api_id


@pytest.fixture(scope="session")
def api_endpoint(api_id):
    client = boto3.client("apigatewayv2")
    apis = client.get_apis()["Items"]
    endpoint = next(api["ApiEndpoint"] for api in apis if api["ApiId"] == api_id)
    print(f"Using endpoint [{endpoint}]")
    return endpoint


def generate_ephemeral_stack_name():
    prefix = os.getenv("STACK_NAME_PREFIX") or f"{DEFAULT_NAME}-it"
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{timestamp}"
