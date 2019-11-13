"""Tests for check_read_only helper."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "spec",
    [
        {"readOnly": True, "x-backref-column": "id"},
        {"readOnly": True, "type": "object", "x-backref-column": "id"},
        {"readOnly": True, "type": "array", "x-backref-column": "id"},
        {"readOnly": True, "type": "array", "items": {}, "x-backref-column": "id"},
        {
            "readOnly": True,
            "type": "array",
            "items": {"type": "object"},
            "x-backref-column": "id",
        },
        {
            "readOnly": True,
            "type": "array",
            "items": {"type": "array"},
            "x-backref-column": "id",
        },
        {"readOnly": True, "type": "simple_type"},
    ],
    ids=[
        "no type",
        "object",
        "array no items",
        "array no items type",
        "array no items type object",
        "array no items type array",
        "x-backref-column missing",
    ],
)
@pytest.mark.column
def test_check_read_only_malformed(spec):
    """
    GIVEN malformed spec
    WHEN check_read_only is called
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.check_read_only(spec=spec)


@pytest.mark.parametrize(
    "spec, expected_result",
    [
        ({}, False),
        ({"readOnly": False}, False),
        ({"readOnly": True, "type": "simple_type", "x-backref-column": "id"}, True),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {"type": "simple_type"},
                "x-backref-column": "id",
            },
            True,
        ),
    ],
    ids=["readOnly missing", "readOnly false", "readOnly true", "readOnly array true"],
)
@pytest.mark.column
def test_check_read_only(spec, expected_result):
    """
    GIVEN spec and expected check result
    WHEN check_read_only is called
    THEN the expected result is returned.
    """
    result = helpers.check_read_only(spec=spec)

    assert result == expected_result
