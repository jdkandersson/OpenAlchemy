"""Tests for artifacts."""
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
                "items": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Ref1"},
                        {"$ref": "#/Components/schemas/Ref2"},
                    ]
                },
            },
            {"Ref1": {"type": "object"}, "Ref2": {"type": "object"}},
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
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "nullable": True,
                }
            },
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "nullable": False,
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
        "nullable True",
        "nullable False",
    ],
)
@pytest.mark.column
def test_invalid(schema, schemas):
    """
    GIVEN array schema that is not valid and schemas
    WHEN gather is called
    THEN MalformedRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedRelationshipError):
        array_ref._artifacts.gather(
            schema=schema, schemas=schemas, logical_name="ref_schema"
        )


@pytest.mark.parametrize(
    "schema, schemas",
    [
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        ),
        (
            {"$ref": "#/components/schemas/Schema"},
            {
                "Schema": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                },
                "RefSchema": {"type": "object", "x-tablename": "ref_schema"},
            },
        ),
        (
            {
                "allOf": [
                    {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                ]
            },
            {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        ),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            },
            {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"allOf": [{"type": "object", "x-tablename": "ref_schema"}]}},
        ),
    ],
    ids=[
        "array items $ref",
        "$ref array items $ref",
        "allOf array items $ref",
        "array items allOf $ref",
        "array items $ref allOf",
    ],
)
@pytest.mark.column
def test_valid(schema, schemas):
    """
    GIVEN array schema and schemas
    WHEN gather is called with the schema and schemas
    THEN artifacts from the array schema are returned.
    """
    artifacts = array_ref._artifacts.gather(
        schema=schema, schemas=schemas, logical_name="ref_schema"
    )

    assert artifacts.relationship.model_name == "RefSchema"
    assert artifacts.spec == {"type": "object", "x-tablename": "ref_schema"}
    assert artifacts.fk_column == "id"
