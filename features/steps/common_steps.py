from behave import given, when, then


@given("the API is available")
def step_api_available(context):
    context.response = None


@when('I send a GET request to "{endpoint}"')
def step_get(context, endpoint):
    context.response = context.client.get(endpoint)


@when('I filter "{endpoint}" by "{key}" equal to "{value}"')
def step_get_with_param(context, endpoint, key, value):
    context.response = context.client.get(endpoint, params={key: value})


@when('I send a DELETE request to "{endpoint}"')
def step_delete(context, endpoint):
    context.response = context.client.delete(endpoint)


@then("the response status code should be {code:d}")
def step_status_code(context, code):
    actual = context.response.status_code
    assert actual == code, f"Expected {code}, got {actual}"


@then('the response field "{field}" should be "{expected}"')
def step_field_value(context, field, expected):
    data = context.response.json()
    actual = str(data.get(field, ""))
    assert actual == expected, f"Field '{field}': expected '{expected}', got '{actual}'"
