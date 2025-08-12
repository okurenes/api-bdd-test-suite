Feature: Todos API
  As an API consumer
  I want to query todo items with different filters
  So that I can retrieve completed and pending tasks accurately

  Background:
    Given the API is available

  @smoke
  Scenario: Retrieve all todos
    When I send a GET request to "/todos"
    Then the response status code should be 200
    And the response should contain 200 todos
    And each todo should have "id", "userId", "title" and "completed" fields

  @regression
  Scenario: Retrieve only completed todos
    When I filter "/todos" by "completed" equal to "true"
    Then the response status code should be 200
    And all todos in response should have "completed" equal to true

  @regression
  Scenario: Retrieve only pending todos
    When I filter "/todos" by "completed" equal to "false"
    Then the response status code should be 200
    And all todos in response should have "completed" equal to false

  @regression
  Scenario: Retrieve todos for a specific user
    When I filter "/todos" by "userId" equal to "1"
    Then the response status code should be 200
    And all todos in response should belong to user 1

  @smoke
  Scenario: Retrieve a single todo
    When I send a GET request to "/todos/1"
    Then the response status code should be 200
    And the todo schema should be valid
