import pytest

from config.endpoints import AUTH, BOOKING, BOOKING_BY_ID
from utils.json_reader import read_json


def test_create_token_with_invalid_credentials(api_client):

    data = {
        "username": "invalid_user",
        "password": "invalid_password"
    }

    response = api_client.post(
        AUTH,
        data=data
    )

    assert response.status == 200

    response_body = response.json()

    assert "reason" in response_body
    assert response_body["reason"] == "Bad credentials"


def test_get_booking_with_invalid_id(api_client):

    response = api_client.get(
        BOOKING_BY_ID.format(99999999)
    )

    assert response.status == 404


def test_get_booking_with_invalid_id_format(api_client):

    response = api_client.get(
        BOOKING_BY_ID.format("abc")
    )

    assert response.status == 404


def test_delete_booking_without_token(api_client, created_booking):

    booking_id = created_booking["booking_id"]

    response = api_client.delete(
        BOOKING_BY_ID.format(booking_id)
    )

    assert response.status in [401, 403]


def test_patch_booking_without_token(api_client, created_booking):

    booking_id = created_booking["booking_id"]

    patch_data = {
        "firstname": "Unauthorized",
        "lastname": "User"
    }

    response = api_client.patch(
        BOOKING_BY_ID.format(booking_id),
        data=patch_data
    )

    assert response.status in [401, 403]


def test_put_booking_without_token(api_client, created_booking):

    booking_id = created_booking["booking_id"]

    put_data = {
        "firstname": "Unauthorized",
        "lastname": "User",
        "totalprice": 1000,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-09-01",
            "checkout": "2026-09-10"
        },
        "additionalneeds": "Breakfast"
    }

    response = api_client.put(
        BOOKING_BY_ID.format(booking_id),
        data=put_data
    )

    assert response.status in [401, 403]


def test_create_booking_with_invalid_payload(api_client):

    data = {
        "firstname": "Sibun"
    }

    response = api_client.post(
        BOOKING,
        data=data
    )

    assert response.status in [400, 500]


def test_create_booking_with_empty_payload(api_client):

    response = api_client.post(
        BOOKING,
        data={}
    )

    assert response.status in [400, 500]