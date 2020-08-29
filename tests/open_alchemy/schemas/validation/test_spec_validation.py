"""Tests for spec validation."""

import pytest

from open_alchemy.schemas import validation

CHECK_TESTS = [
    pytest.param(
        True,
        (False, "specification must be a dictionary"),
        id="spec not dict",
    ),
    pytest.param(
        {},
        (False, "specification must define components"),
        id="no components key",
    ),
    pytest.param(
        {"components": True},
        (False, "components value must be a dictionary"),
        id="components value not dict",
    ),
    pytest.param(
        {"components": {}},
        (False, "specification must define schemas"),
        id="no schemas",
    ),
    pytest.param(
        {"components": {"schemas": True}},
        (False, "schemas must be a dictionary"),
        id="schemas not dict",
    ),
    pytest.param(
        {"components": {"schemas": {}}},
        (True, None),
        id="schemas valid",
    ),
]


@pytest.mark.parametrize("spec, expected_result", CHECK_TESTS)
@pytest.mark.schemas
def test_check(spec, expected_result):
    """
    GIVEN spec and the expected result
    WHEN check is called with the spec
    THEN the expected result is returned.
    """
    returned_result = validation.spec_validation.check(spec=spec)

    assert returned_result == expected_result
