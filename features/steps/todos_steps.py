from behave import then
from utils import schema_validator


@then("the response should contain {count:d} todos")
def step_todo_count(context, count):
    data = context.response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) == count, f"Expected {count} todos, got {len(data)}"


@then('each todo should have "id", "userId", "title" and "completed" fields')
def step_todo_fields(context):
    for todo in context.response.json():
        for field in ("id", "userId", "title", "completed"):
            assert field in todo, f"Field '{field}' missing in todo: {todo}"


@then('all todos in response should have "completed" equal to {expected}')
def step_todos_completed_filter(context, expected):
    expected_bool = expected.strip().lower() == "true"
    todos = context.response.json()
    assert len(todos) > 0, "No todos returned"
    for todo in todos:
        assert todo["completed"] == expected_bool, \
            f"Todo {todo['id']} has completed={todo['completed']}, expected {expected_bool}"


@then("all todos in response should belong to user {user_id:d}")
def step_todos_belong_to_user(context, user_id):
    todos = context.response.json()
    assert len(todos) > 0, "No todos returned"
    for todo in todos:
        assert todo["userId"] == user_id, \
            f"Todo {todo['id']} belongs to user {todo['userId']}, not {user_id}"


@then("the todo schema should be valid")
def step_todo_schema(context):
    schema_validator.validate(context.response.json(), schema_validator.TODO_SCHEMA)
