import json
from urllib.parse import urlparse, parse_qs
import responses as resp_mock
from utils.api_client import APIClient

BASE = "https://jsonplaceholder.typicode.com"

_USERS = [{"id": i, "name": f"User {i}", "username": f"user{i}", "email": f"user{i}@example.com"} for i in range(1, 11)]
_USERS[0] = {"id": 1, "name": "Leanne Graham", "username": "Bret", "email": "Sincere@april.biz"}

_POSTS = [{"id": i, "userId": ((i - 1) // 10) + 1, "title": f"Post {i}", "body": f"Body {i}"} for i in range(1, 101)]
_TODOS = [{"id": i, "userId": ((i - 1) // 20) + 1, "title": f"Todo {i}", "completed": i % 2 == 0} for i in range(1, 201)]


def _posts_callback(request):
    params = parse_qs(urlparse(request.url).query)
    data = _POSTS
    if "userId" in params:
        uid = int(params["userId"][0])
        data = [p for p in _POSTS if p["userId"] == uid]
    return 200, {"Content-Type": "application/json"}, json.dumps(data)


def _todos_callback(request):
    params = parse_qs(urlparse(request.url).query)
    data = _TODOS
    if "completed" in params:
        val = params["completed"][0].lower() == "true"
        data = [t for t in _TODOS if t["completed"] == val]
    if "userId" in params:
        uid = int(params["userId"][0])
        data = [t for t in data if t["userId"] == uid]
    return 200, {"Content-Type": "application/json"}, json.dumps(data)


def before_scenario(context, scenario):
    context.mock = resp_mock.RequestsMock(assert_all_requests_are_fired=False)
    context.mock.start()
    context.client = APIClient()
    context.payload = {}

    # Users
    context.mock.add(resp_mock.GET, f"{BASE}/users", json=_USERS, status=200)
    context.mock.add(resp_mock.GET, f"{BASE}/users/1", json=_USERS[0], status=200)
    context.mock.add(resp_mock.GET, f"{BASE}/users/9999", json={}, status=404)
    context.mock.add(resp_mock.PUT, f"{BASE}/users/1",
                     json={"id": 1, "name": "Updated Name", "email": "updated@example.com"}, status=200)
    context.mock.add(resp_mock.DELETE, f"{BASE}/users/1", json={}, status=200)

    # Posts — callback handles query param filtering
    context.mock.add_callback(resp_mock.GET, f"{BASE}/posts", _posts_callback)
    context.mock.add(resp_mock.GET, f"{BASE}/posts/1", json=_POSTS[0], status=200)
    context.mock.add(resp_mock.POST, f"{BASE}/posts",
                     json={"id": 101, "title": "BDD Testing with Behave",
                           "body": "Writing clean Gherkin tests", "userId": 1},
                     status=201)

    # Todos — callback handles query param filtering
    context.mock.add_callback(resp_mock.GET, f"{BASE}/todos", _todos_callback)
    context.mock.add(resp_mock.GET, f"{BASE}/todos/1", json=_TODOS[0], status=200)


def after_scenario(context, scenario):
    context.mock.stop()
    context.mock.reset()
