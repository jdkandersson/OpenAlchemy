"""Tests for check_read_only helper."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "spec",
    [
        {"readOnly": True},
        {"readOnly": True, "type": "simple_type"},
        {"readOnly": True, "type": "array"},
        {"readOnly": True, "type": "array", "items": {}},
        {"readOnly": True, "type": "array", "items": {"type": "simple_type"}},
        {"readOnly": True, "type": "array", "items": {"type": "array"}},
        {"readOnly": True, "type": "object"},
        {"readOnly": True, "type": "object", "properties": {}},
        {"readOnly": True, "type": "object", "properties": {"key": {"type": "array"}}},
        {"readOnly": True, "type": "object", "properties": {"key": {"type": "object"}}},
    ],
    ids=[
        "no type",
        "not object nor array",
        "array no items",
        "array no items type",
        "array items type not object nor array",
        "array items type array",
        "object no properties",
        "object empty properties",
        "object property type array",
        "object property type object",
    ],
)
@pytest.mark.helper
def test_malformed(spec):
    """
    GIVEN malformed spec
    WHEN check_read_only is called
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.check_read_only(spec=spec, schemas={})


@pytest.mark.parametrize(
    "spec, schemas, expected_result",
    [
        ({}, {}, False),
        ({"readOnly": False}, {}, False),
        (
            {
                "readOnly": True,
                "type": "object",
                "properties": {"key": {"type": "simple_type"}},
            },
            {},
            True,
        ),
        (
            {
                "readOnly": True,
                "type": "object",
                "properties": {"key": {"$ref": "#/components/schemas/Key"}},
            },
            {"Key": {"type": "simple_type"}},
            True,
        ),
        (
            {
                "readOnly": True,
                "type": "object",
                "properties": {"key": {"allOf": [{"type": "simple_type"}]}},
            },
            {},
            True,
        ),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"key": {"type": "simple_type"}},
                },
            },
            {},
            True,
        ),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {"$ref": "#/components/schemas/Schema"},
            },
            {
                "Schema": {
                    "type": "object",
                    "properties": {"key": {"type": "simple_type"}},
                }
            },
            True,
        ),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {
                    "allOf": [
                        {
                            "type": "object",
                            "properties": {"key": {"type": "simple_type"}},
                        }
                    ]
                },
            },
            {},
            True,
        ),
    ],
    ids=[
        "readOnly missing",
        "readOnly false",
        "readOnly true",
        "readOnly true object property $ref",
        "readOnly true object property allOf",
        "readOnly true array",
        "readOnly true array items $ref",
        "readOnly true array items allOf",
    ],
)
@pytest.mark.helper
def test_valid(spec, schemas, expected_result):
    """
    GIVEN spec and expected check result
    WHEN check_read_only is called
    THEN the expected result is returned.
    """
    result = helpers.check_read_only(spec=spec, schemas=schemas)

    assert result == expected_result
