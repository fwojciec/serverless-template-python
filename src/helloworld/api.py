from typing import Any, Dict, TypedDict


LambdaDict = Dict[str, Any]


class APIGatewayProxyResponse(TypedDict):
    statusCode: int
    body: str


def handler(event: LambdaDict, _context: LambdaDict) -> APIGatewayProxyResponse:
    return {
        "statusCode": 200,
        "body": "Hello World",
    }
