import pytest

from config.endpoints import BOOKING, BOOKING_BY_ID
from utils.json_reader import read_json


def test_create_booking(api_client):

    data = read_json("testdata/post_request_body.json")

    response = api_client.post(
        BOOKING,
        data=data
    )

    assert response.status == 200

    response_body = response.json()

    assert "bookingid" in response_body
    assert "booking" in response_body

    assert response_body["booking"]["firstname"] == data["firstname"]
    assert response_body["booking"]["lastname"] == data["lastname"]
    assert response_body["booking"]["totalprice"] == data["totalprice"]
    assert response_body["booking"]["depositpaid"] == data["depositpaid"]


def test_booking_by_id(api_client, created_booking):

    booking_id = created_booking["booking_id"]

    response = api_client.get(
        BOOKING_BY_ID.format(booking_id)
    )

    assert response.status == 200

    response_body = response.json()

    assert "firstname" in response_body
    assert "lastname" in response_body

    assert response_body["firstname"] == \
        created_booking["booking"]["firstname"]

    assert response_body["lastname"] == \
        created_booking["booking"]["lastname"]


def test_booking_by_name(api_client, created_booking):

    data = created_booking["request_data"]

    params = {
        "firstname": data["firstname"],
        "lastname": data["lastname"],
    }

    response = api_client.get(
        BOOKING,
        params=params
    )

    assert response.status == 200

    response_body = response.json()

    assert isinstance(response_body, list)
    assert len(response_body) > 0

    booking_ids = [
        item["bookingid"]
        for item in response_body
    ]

    assert created_booking["booking_id"] in booking_ids


@pytest.mark.xfail(
    reason="Restful Booker date filtering does not reliably return matching bookings"
)
def test_booking_by_dates(api_client, created_booking):

    dates = created_booking["request_data"]["bookingdates"]

    response = api_client.get(
        BOOKING,
        params=dates
    )

    assert response.status == 200

    response_body = response.json()

    print("Date filter parameters:", dates)
    print("Date filter response:", response_body)

    assert isinstance(response_body, list)

    booking_ids = [
        item["bookingid"]
        for item in response_body
    ]

    assert created_booking["booking_id"] in booking_ids


def test_patch_booking(api_client, created_booking, auth_token):

    booking_id = created_booking["booking_id"]

    patch_data = {
        "firstname": "SibunUpdated",
        "lastname": "KatualaUpdated"
    }

    response = api_client.patch(
        BOOKING_BY_ID.format(booking_id),
        data=patch_data,
        token=auth_token
    )

    assert response.status == 200

    response_body = response.json()

    assert response_body["firstname"] == patch_data["firstname"]
    assert response_body["lastname"] == patch_data["lastname"]

    get_response = api_client.get(
        BOOKING_BY_ID.format(booking_id)
    )

    assert get_response.status == 200

    get_response_body = get_response.json()

    assert get_response_body["firstname"] == patch_data["firstname"]
    assert get_response_body["lastname"] == patch_data["lastname"]


def test_put_booking(api_client, created_booking, auth_token):

    booking_id = created_booking["booking_id"]

    put_data = {
        "firstname": "SibunPUT",
        "lastname": "KatualaPUT",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-09-01",
            "checkout": "2026-09-10"
        },
        "additionalneeds": "Breakfast"
    }

    response = api_client.put(
        BOOKING_BY_ID.format(booking_id),
        data=put_data,
        token=auth_token
    )

    assert response.status == 200

    response_body = response.json()

    assert response_body["firstname"] == put_data["firstname"]
    assert response_body["lastname"] == put_data["lastname"]
    assert response_body["totalprice"] == put_data["totalprice"]
    assert response_body["depositpaid"] == put_data["depositpaid"]
    assert response_body["bookingdates"] == put_data["bookingdates"]
    assert response_body["additionalneeds"] == put_data["additionalneeds"]

    get_response = api_client.get(
        BOOKING_BY_ID.format(booking_id)
    )

    assert get_response.status == 200

    get_response_body = get_response.json()

    assert get_response_body["firstname"] == put_data["firstname"]
    assert get_response_body["lastname"] == put_data["lastname"]
    assert get_response_body["totalprice"] == put_data["totalprice"]
    assert get_response_body["depositpaid"] == put_data["depositpaid"]
    assert get_response_body["bookingdates"] == put_data["bookingdates"]
    assert get_response_body["additionalneeds"] == put_data["additionalneeds"]


def test_delete_booking(api_client, created_booking, auth_token):

    booking_id = created_booking["booking_id"]

    response = api_client.delete(
        BOOKING_BY_ID.format(booking_id),
        token=auth_token
    )

    assert response.status == 201

    get_response = api_client.get(
        BOOKING_BY_ID.format(booking_id)
    )

    assert get_response.status == 404