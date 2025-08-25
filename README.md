# API BDD Test Suite

[![CI](https://github.com/okurenes/api-bdd-test-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/okurenes/api-bdd-test-suite/actions)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Behave](https://img.shields.io/badge/BDD-Behave-brightgreen)
![Scenarios](https://img.shields.io/badge/scenarios-17-blue)
![Steps](https://img.shields.io/badge/steps-81-blue)

A **BDD (Behaviour-Driven Development)** API test suite built with [Behave](https://behave.readthedocs.io/) and Gherkin. Tests are written in plain English, mocked end-to-end with the `responses` library — zero external HTTP calls, zero flakiness.

Target API: [JSONPlaceholder](https://jsonplaceholder.typicode.com) (users, posts, todos).

---

## What's Inside

| Feature file | Scenarios | Tags |
|---|---|---|
| `users.feature` | 8 | `@smoke`, `@regression` |
| `posts.feature` | 4 | `@smoke`, `@regression` |
| `todos.feature` | 5 | `@smoke`, `@regression` |

**17 scenarios · 81 steps · all passing**

---

## Key Patterns

- **Gherkin scenarios** — Background, Scenario, Scenario Outline + Examples table
- **Callback-based mocks** — `responses.RequestsMock` with callback functions that parse query params for dynamic filtering (e.g. `?userId=1`, `?completed=true`)
- **Per-scenario mock injection** — step definitions add dynamic mocks to `context.mock` at runtime
- **Tag-based execution** — smoke tests run first in CI, full suite runs second
- **Allure reporting** — structured HTML reports via `allure-behave`

---

## Project Structure

```
features/
├── users.feature          # User CRUD scenarios
├── posts.feature          # Post create/retrieve scenarios
├── todos.feature          # Todo filter scenarios
├── environment.py         # before/after_scenario hooks + HTTP mocks
└── steps/
    ├── common_steps.py    # Shared steps: GET/POST/DELETE, status code, field assertions
    ├── users_steps.py     # User-specific steps + dynamic POST mock
    ├── posts_steps.py     # Post-specific steps + table payload parsing
    └── todos_steps.py     # Todo-specific steps + filter assertions

utils/
├── api_client.py          # Thin requests wrapper (base URL, logging)
└── schema_validator.py    # JSON schema definitions + validate()

config/
└── settings.py            # Base URL, timeout config

.github/workflows/
└── ci.yml                 # Run @smoke first, then full suite; upload Allure results
```

---

## Setup

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run Tests

```bash
# All tests
behave --no-capture

# Smoke tests only
behave --tags=@smoke --no-capture

# Regression tests only
behave --tags=@regression --no-capture

# With Allure output
behave -f allure_behave.formatter:AllureFormatter -o allure-results --no-capture
```

---

## How Mocking Works

HTTP calls are intercepted at the scenario level using `responses.RequestsMock`:

```python
# environment.py — before_scenario hook
context.mock = responses.RequestsMock(assert_all_requests_are_fired=False)
context.mock.start()

# Callback for dynamic query param filtering
def _posts_callback(request):
    params = parse_qs(urlparse(request.url).query)
    data = [p for p in _POSTS if p["userId"] == int(params["userId"][0])] \
           if "userId" in params else _POSTS
    return 200, {"Content-Type": "application/json"}, json.dumps(data)

context.mock.add_callback(responses.GET, f"{BASE}/posts", _posts_callback)
```

Step definitions can add further mocks dynamically:

```python
# users_steps.py — per-scenario POST mock
@when('I create a user with name "{name}" and email "{email}"')
def step_create_user(context, name, email):
    context.mock.add(responses.POST, f"{BASE}/users",
                     json={"id": 11, "name": name, "email": email}, status=201)
    context.response = context.client.post("/users", payload={"name": name, "email": email})
```

---

## Example Feature

```gherkin
Feature: User Management API

  Background:
    Given the API is available

  @smoke
  Scenario: Retrieve the full list of users
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should contain 10 users
    And each user should have "id", "name" and "email" fields

  @regression
  Scenario Outline: Create users with different profiles
    When I create a user with name "<name>" and email "<email>"
    Then the response status code should be 201
    And the response field "name" should be "<name>"
    And a new user "id" should be returned

    Examples:
      | name        | email             |
      | Enes Okur   | enes@example.com  |
      | Jane Smith  | jane@example.com  |
      | Bob Johnson | bob@example.com   |
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| `behave==1.2.6` | BDD test runner |
| `requests==2.31.0` | HTTP client |
| `responses==0.25.3` | HTTP mocking |
| `jsonschema==4.20.0` | Response schema validation |
| `allure-behave==2.13.2` | Allure report formatter |
| GitHub Actions | CI/CD pipeline |

---

## License

Portfolio / educational project — free to use.
