Feature: Initialize luucy-python
  Initializing `LUUCY` luucy-python in a python project

  Scenario: Can be initialized with username and password

    Given that luucy-python is installed
    When a username and password are set
    Then it loads successfully

  Scenario: Raises an exception if no username and password are supplied

    Given that luucy-python is installed
    When no username and password are set
    Then it raises and exception

  Scenario: Can be initialized with environment username and password

    Given that luucy-python is installed
    When a usernamane and password are set via LUUCY_USERNAME and LUUCY_PASSWORD environment variables
    Then it loads successfully

  Scenario: Returns user data

    Given the client is logged in
    When user_data is called
    Then user data of logged in user is returned

  Scenario: Can be used with different environments

    Given the baseUrl is set to staging
    When initiating the client
    Then staging is used

  Scenario: Can be used with production environment

    Given the baseUrl is set not set
    When initiating the client
    Then production is used
