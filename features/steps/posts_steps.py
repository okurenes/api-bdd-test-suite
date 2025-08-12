from behave import given, when, then
from utils import schema_validator


@then("the response should contain {count:d} posts")
def step_post_count(context, count):
    data = context.response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) == count, f"Expected {count} posts, got {len(data)}"


@then('each post should have "id", "title", "body" and "userId" fields')
def step_post_fields(context):
    for post in context.response.json():
        for field in ("id", "title", "body", "userId"):
            assert field in post, f"Field '{field}' missing in post: {post}"


@then("all posts in response should belong to user {user_id:d}")
def step_posts_belong_to_user(context, user_id):
    posts = context.response.json()
    assert len(posts) > 0, "No posts returned"
    for post in posts:
        assert post["userId"] == user_id, f"Post {post['id']} belongs to user {post['userId']}, not {user_id}"


@given("I have a post payload")
def step_post_payload(context):
    context.payload = {row["field"]: row["value"] for row in context.table}
    if "userId" in context.payload:
        context.payload["userId"] = int(context.payload["userId"])


@when('I send a POST request to "{endpoint}" with the payload')
def step_post_with_payload(context, endpoint):
    context.response = context.client.post(endpoint, payload=context.payload)


@then("the post schema should be valid")
def step_post_schema(context):
    schema_validator.validate(context.response.json(), schema_validator.POST_SCHEMA)
