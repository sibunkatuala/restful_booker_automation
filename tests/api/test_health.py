from config.endpoints import PING


def test_health_check(api_client):

    response = api_client.get(
        PING
    )

    assert response.status == 201