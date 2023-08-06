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
