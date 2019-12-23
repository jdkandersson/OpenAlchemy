"""Tests for gather_array_artifacts."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy.column_factory import array_ref


@pytest.mark.parametrize(
    "schema, schemas",
    [
        ({"type": "array"}, {}),
        ({"type": "array", "items": {}}, {}),
        ({"type": "array", "items": {"allOf": []}}, {}),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "ref 1"}, {"$ref": "ref 2"}]},
            },
            {},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
        ),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            },
            {"RefSchema": {}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "integer"}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "object"}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "x-backref": "schema",
                    "x-uselist": False,
                }
            },
        ),
    ],
    ids=[
        "no items",
        "items without $ref and allOf",
        "items allOf without $ref",
        "items allOf multiple $ref",
        "$ref items no type",
        "allOf items no type",
        "items type not object",
        "items no x-tablename",
        "backref and uselist defined",
    ],
)
@pytest.mark.column
def test_handle_array_invalid(schema, schemas):
    """
    GIVEN array schema that is not valid and schemas
    WHEN handle_array is called
    THEN MalformedRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedRelationshipError):
        array_ref._gather_array_artifacts.gather_array_artifacts(
            schema=schema, schemas=schemas, logical_name="ref_schema"
        )
