"""Test the Gherkin formatter."""

import pytest
from reformat_gherkin.errors import InvalidInput

#  given

unformatted = """Feature: Test feature
Scenario: Test scenario
Given I have a test
When I run the test
Then it should pass
"""

unformatted_simple = """```gherkin
Feature: Test feature
Scenario: Test scenario
Given I have a test
When I run the test
Then it should pass
```"""

unformatted_background = """```gherkin
Feature: Test feature
Background:
Given I am logged in
Scenario: Test scenario
When I do something
Then it should work
```"""

unformatted_outlined = """```gherkin
Feature: Test feature
Scenario Outline: Test scenario
Given I have a test
When I run the <key>
Then it should pass
Examples:
|key|
|test|
```"""

# then

expected = """Feature: Test feature

  Scenario: Test scenario
    Given I have a test
    When  I run the test
    Then  it should pass
"""

expected_simple = """```gherkin
Feature: Test feature

  Scenario: Test scenario
    Given I have a test
    When  I run the test
    Then  it should pass
```
"""

expected_background = """```gherkin
Feature: Test feature

  Background:
    Given I am logged in

  Scenario: Test scenario
    When  I do something
    Then  it should work
```
"""

expected_outlined = """```gherkin
Feature: Test feature

  Scenario Outline: Test scenario
    Given I have a test
    When  I run the <key>
    Then  it should pass

    Examples:
      | key  |
      | test |
```
"""


def test_format_gherkin():
    # Import the module directly to test the format_gherkin function
    import mdformat_gherkin

    # Test case 1: Simple formatting
    formatted = mdformat_gherkin.format_gherkin(unformatted, "")
    assert formatted == expected, f"\nExpected:\n{expected!r}\n\nGot:\n{formatted!r}"

    # Test case 2: Empty input should return empty string
    empty_result = mdformat_gherkin.format_gherkin("", "")
    assert empty_result == "", "Empty input should return empty string"

    # Test case 3: Invalid Gherkin syntax should throw an InvalidInput
    invalid_gherkin = "This is not valid Gherkin"
    with pytest.raises(InvalidInput):
        mdformat_gherkin.format_gherkin(invalid_gherkin, "")


def test_mdformat_integration():
    # Import here to ensure we're testing the installed package
    import mdformat

    # Test case 1: Simple feature
    # Run the formatter
    formatted = mdformat.text(unformatted_simple, codeformatters={"gherkin"})

    # Compare the normalized outputs
    assert (
        formatted == expected_simple
    ), f"\nExpected:\n{expected_simple!r}\n\nGot:\n{formatted!r}"

    # Test case 2: Feature with background
    # Run the formatter
    formatted = mdformat.text(unformatted_background, codeformatters={"gherkin"})

    # Compare the normalized outputs
    assert (
        formatted == expected_background
    ), f"\nExpected:\n{expected_background!r}\n\nGot:\n{formatted!r}"

    # Test case 3: Feature with outlined scenario
    # Run the formatter
    formatted = mdformat.text(unformatted_outlined, codeformatters={"gherkin"})

    # Compare the normalized outputs
    assert (
        formatted == expected_outlined
    ), f"\nExpected:\n{expected_outlined!r}\n\nGot:\n{formatted!r}"
