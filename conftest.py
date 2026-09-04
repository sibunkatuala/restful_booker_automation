import pytest
from playwright.sync_api import Playwright

from utils.api_client import APIClient
from utils.json_reader import read_json
from utils.logger import setup_logging
from config.endpoints import AUTH, BOOKING


@pytest.fixture(scope="session", autouse=True)
def configure_logging():

    setup_logging()


@pytest.fixture(scope="session")
def request_context(playwright: Playwright):

    context = playwright.request.new_context()

    yield context

    context.dispose()


@pytest.fixture(scope="session")
def api_client(request_context):

    return APIClient(request_context)


@pytest.fixture(scope="session")
def auth_token(api_client):

    data = read_json("testdata/token_request_body.json")

    response = api_client.post(
        AUTH,
        data=data
    )

    assert response.status == 200

    response_body = response.json()

    assert "token" in response_body
    assert response_body["token"]

    return response_body["token"]


@pytest.fixture(scope="session")
def created_booking(api_client):

    data = read_json("testdata/post_request_body.json")

    response = api_client.post(
        BOOKING,
        data=data
    )

    assert response.status == 200

    response_body = response.json()

    assert "bookingid" in response_body
    assert "booking" in response_body

    return {
        "booking_id": response_body["bookingid"],
        "booking": response_body["booking"],
        "request_data": data,
    }