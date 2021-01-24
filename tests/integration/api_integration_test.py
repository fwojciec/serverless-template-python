import requests


def test_api_endpoint_status_and_content(api_endpoint):
    assert api_endpoint != ""
    result = requests.get(api_endpoint)
    assert result.status_code == 200
    assert result.text == "Hello World"
