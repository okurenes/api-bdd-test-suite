Feature: Posts API
  As an API consumer
  I want to create and retrieve blog posts
  So that content management operations work correctly

  Background:
    Given the API is available

  @smoke
  Scenario: Retrieve all posts
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should contain 100 posts
    And each post should have "id", "title", "body" and "userId" fields

  @smoke
  Scenario: Retrieve posts for a specific user
    When I filter "/posts" by "userId" equal to "1"
    Then the response status code should be 200
    And all posts in response should belong to user 1

  @regression
  Scenario: Create a new post
    Given I have a post payload:
      | field  | value                        |
      | title  | BDD Testing with Behave      |
      | body   | Writing clean Gherkin tests  |
      | userId | 1                            |
    When I send a POST request to "/posts" with the payload
    Then the response status code should be 201
    And the response field "title" should be "BDD Testing with Behave"
    And the post schema should be valid

  @regression
  Scenario: Retrieve a single post
    When I send a GET request to "/posts/1"
    Then the response status code should be 200
    And the response field "userId" should be "1"
    And the post schema should be valid
