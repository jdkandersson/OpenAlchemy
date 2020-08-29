"""Tests for schemas validation."""

import pytest

from open_alchemy.schemas import validation

CHECK_TESTS = [
    pytest.param(True, (False, "schemas must be a dictionary"), id="schemas not dict"),
    pytest.param({}, (True, None), id="schemas empty"),
    pytest.param(
        {True: {}},
        (False, "schemas keys must be strings, True is not"),
        id="schemas key not string",
    ),
    pytest.param(
        {"Schema1": True},
        (False, "the value of Schema1 must be a dictionary"),
        id="schemas values not dict",
    ),
    pytest.param(
        {True: {}, "Schema2": {}},
        (False, "schemas keys must be strings, True is not"),
        id="multiple model first key invalid",
    ),
    pytest.param(
        {"Schema1": {}, True: {}},
        (False, "schemas keys must be strings, True is not"),
        id="multiple model second key invalid",
    ),
    pytest.param(
        {"Schema1": True, "Schema2": {}},
        (False, "the value of Schema1 must be a dictionary"),
        id="multiple model first value invalid",
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": True},
        (False, "the value of Schema2 must be a dictionary"),
        id="multiple model second value invalid",
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": {}},
        (True, None),
        id="multiple model valid",
    ),
]


@pytest.mark.parametrize("schemas, expected_result", CHECK_TESTS)
@pytest.mark.schemas
def test_check(schemas, expected_result):
    """
    GIVEN schemas and the expected result
    WHEN check is called with the schemas
    THEN the expected result is returned.
    """
    returned_result = validation.schemas_validation.check(schemas=schemas)

    assert returned_result == expected_result
