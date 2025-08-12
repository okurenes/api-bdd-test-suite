Feature: User Management API
  As an API consumer
  I want to manage users through the REST API
  So that I can perform full CRUD operations reliably

  Background:
    Given the API is available

  @smoke
  Scenario: Retrieve the full list of users
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should contain 10 users
    And each user should have "id", "name" and "email" fields

  @smoke
  Scenario: Retrieve a specific user by ID
    When I send a GET request to "/users/1"
    Then the response status code should be 200
    And the response field "name" should be "Leanne Graham"
    And the response field "email" should be "Sincere@april.biz"
    And the user schema should be valid

  @regression
  Scenario: Request a non-existent user returns 404
    When I send a GET request to "/users/9999"
    Then the response status code should be 404

  @regression
  Scenario Outline: Create users with different profiles
    When I create a user with name "<name>" and email "<email>"
    Then the response status code should be 201
    And the response field "name" should be "<name>"
    And the response field "email" should be "<email>"
    And a new user "id" should be returned

    Examples:
      | name           | email                  |
      | Enes Okur      | enes@example.com       |
      | Jane Smith     | jane@example.com       |
      | Bob Johnson    | bob@example.com        |

  @regression
  Scenario: Update an existing user
    When I update user 1 with name "Updated Name" and email "updated@example.com"
    Then the response status code should be 200
    And the response field "name" should be "Updated Name"
    And the response field "email" should be "updated@example.com"

  @regression
  Scenario: Delete a user
    When I send a DELETE request to "/users/1"
    Then the response status code should be 200
