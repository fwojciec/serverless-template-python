import os
import pytest
import boto3


@pytest.fixture(scope="session")
def stack_name():
    stack_name = os.getenv("STACK_NAME")
    if stack_name is None:
        user = os.environ["USER"]
        stack_name = f"serverless-template-python-{user}"
    print(f"Using stack [{stack_name}]")
    return stack_name


@pytest.fixture(scope="session")
def api_id(stack_name):
    client = boto3.client("cloudformation")
    outs = client.describe_stacks(StackName=stack_name)["Stacks"][0]["Outputs"]
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
