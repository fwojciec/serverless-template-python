from src.helloworld.api import handler


def test_api_returns_expected_message():
    result = handler({}, {})
    expected = {"statusCode": 200, "body": "Hello World"}
    assert result == expected
