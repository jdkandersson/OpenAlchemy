"""Tests for check_read_only helper."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "spec, schemas",
    [
        ({"readOnly": True, "x-backref-column": "id"}, None),
        ({"readOnly": True, "type": "object", "x-backref-column": "id"}, None),
        ({"readOnly": True, "type": "array", "x-backref-column": "id"}, {}),
        (
            {"readOnly": True, "type": "array", "items": {}, "x-backref-column": "id"},
            {},
        ),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {"type": "object"},
                "x-backref-column": "id",
            },
            {},
        ),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {"type": "array"},
                "x-backref-column": "id",
            },
            {},
        ),
        ({"readOnly": True, "type": "simple_type"}, None),
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
@pytest.mark.helper
def test_malformed(spec, schemas):
    """
    GIVEN malformed spec
    WHEN check_read_only is called
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.check_read_only(spec=spec, schemas=schemas)


@pytest.mark.parametrize(
    "spec, schemas, expected_result",
    [
        ({}, None, False),
        ({"readOnly": False}, None, False),
        (
            {"readOnly": True, "type": "simple_type", "x-backref-column": "id"},
            None,
            True,
        ),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {"type": "simple_type"},
                "x-backref-column": "id",
            },
            {},
            True,
        ),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {"$ref": "#/components/schemas/Items"},
                "x-backref-column": "id",
            },
            {"Items": {"type": "simple_type"}},
            True,
        ),
        (
            {
                "readOnly": True,
                "type": "array",
                "items": {"allOf": [{"type": "simple_type"}]},
                "x-backref-column": "id",
            },
            {},
            True,
        ),
    ],
    ids=[
        "readOnly missing",
        "readOnly false",
        "readOnly true",
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


@pytest.mark.helper
def test_array_schemas_none():
    """
    GIVEN array readOnly spec
    WHEN check_read_only with None for schemas
    THEN MissingArgumentError is raised.
    """
    spec = {
        "readOnly": True,
        "type": "array",
        "items": {"type": "simple_type"},
        "x-backref-column": "id",
    }

    with pytest.raises(exceptions.MissingArgumentError):
        helpers.check_read_only(spec=spec)
