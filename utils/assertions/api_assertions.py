def assert_status(response, expected_status):

    actual_status = response.status

    assert actual_status == expected_status, (
        f"Expected status {expected_status}, "
        f"but received {actual_status}"
    )


def assert_response_contains(response, key):

    response_body = response.json()

    assert key in response_body, (
        f"Expected '{key}' in response, "
        f"but it was not found"
    )


def assert_response_field(response, field, expected_value):

    response_body = response.json()

    actual_value = response_body.get(field)

    assert actual_value == expected_value, (
        f"Expected {field}={expected_value}, "
        f"but received {actual_value}"
    )