from config.endpoints import AUTH
from utils.json_reader import read_json


def test_create_token(api_client):

    data = read_json("testdata/token_request_body.json")

    response = api_client.post(
        AUTH,
        data=data
    )

    assert response.status == 200

    response_body = response.json()

    assert "token" in response_body
    assert response_body["token"]