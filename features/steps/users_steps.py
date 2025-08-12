import responses as resp_mock
from behave import when, then
from utils import schema_validator

BASE = "https://jsonplaceholder.typicode.com"


@then("the response should contain {count:d} users")
def step_user_count(context, count):
    data = context.response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) == count, f"Expected {count} users, got {len(data)}"


@then('each user should have "id", "name" and "email" fields')
def step_user_fields(context):
    for user in context.response.json():
        for field in ("id", "name", "email"):
            assert field in user, f"Field '{field}' missing in user: {user}"


@then("the user schema should be valid")
def step_user_schema(context):
    schema_validator.validate(context.response.json(), schema_validator.USER_SCHEMA)


@when('I create a user with name "{name}" and email "{email}"')
def step_create_user(context, name, email):
    context.mock.add(
        resp_mock.POST, f"{BASE}/users",
        json={"id": 11, "name": name, "email": email},
        status=201,
    )
    context.response = context.client.post("/users", payload={"name": name, "email": email})


@then('a new user "id" should be returned')
def step_new_user_id(context):
    data = context.response.json()
    assert "id" in data, "No 'id' field in response"
    assert isinstance(data["id"], int), "id is not an integer"


@when('I update user {user_id:d} with name "{name}" and email "{email}"')
def step_update_user(context, user_id, name, email):
    context.response = context.client.put(f"/users/{user_id}", payload={"name": name, "email": email})
