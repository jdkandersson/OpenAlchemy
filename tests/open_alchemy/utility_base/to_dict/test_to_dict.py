"""Tests for to_dict."""

import pytest

from open_alchemy.utility_base import to_dict


@pytest.mark.parametrize(
    "schema, expected_result",
    [
        pytest.param(
            {"properties": {"prop_1": {"key": "value"}}},
            False,
            id="nullable not set required not set expect false",
        ),
        pytest.param(
            {"properties": {"prop_1": {"key": "value"}}, "required": []},
            False,
            id="nullable not set required empty expect false",
        ),
        pytest.param(
            {"properties": {"prop_1": {"key": "value"}}, "required": ["prop_2"]},
            False,
            id="nullable not set required different property expect false",
        ),
        pytest.param(
            {"properties": {"prop_1": {"key": "value"}}, "required": ["prop_1"]},
            True,
            id="nullable not set required has property expect true",
        ),
        pytest.param(
            {
                "properties": {"prop_1": {"key": "value", "nullable": False}},
                "required": [],
            },
            False,
            id="nullable false required empty expect false",
        ),
        pytest.param(
            {
                "properties": {"prop_1": {"key": "value", "nullable": False}},
                "required": ["prop_1"],
            },
            True,
            id="nullable false required has property expect true",
        ),
        pytest.param(
            {
                "properties": {"prop_1": {"key": "value", "nullable": True}},
                "required": [],
            },
            True,
            id="nullable true required empty expect true",
        ),
        pytest.param(
            {
                "properties": {"prop_1": {"key": "value", "nullable": True}},
                "required": ["prop_1"],
            },
            True,
            id="nullable true required has property expect true",
        ),
    ],
)
@pytest.mark.utility_base
def test_return_none(schema, expected_result):
    """
    GIVEN schema with property and expected result
    WHEN return_none is called with the schema and property name
    THEN the expected result is returned.
    """
    result = to_dict.return_none(schema=schema, property_name="prop_1")

    assert result == expected_result
