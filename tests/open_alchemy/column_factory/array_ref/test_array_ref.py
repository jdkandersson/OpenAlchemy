"""Tests for array references."""

import pytest

from open_alchemy.column_factory import array_ref


@pytest.mark.parametrize(
    "spec, schemas",
    [
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {"$ref": "#/components/schemas/Schema"},
            {
                "Schema": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                },
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                },
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
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            },
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "allOf": [
                        {
                            "type": "object",
                            "x-tablename": "ref_schema",
                            "properties": {},
                        }
                    ]
                }
            },
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
def test_handle_array_relationship(spec, schemas):
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN handle_array is called
    THEN relationship is returned pointing to the referenced schema.
    """
    logical_name = "ref_schema"
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }

    ([(tbl_logical_name, relationship)], schema_spec) = array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name=logical_name
    )

    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert relationship.secondary is None
    assert tbl_logical_name == logical_name
    assert schema_spec == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }


@pytest.mark.column
def test_handle_array_schemas():
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN handle_array is called
    THEN foreign key is added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "allOf": [
                {"type": "object", "x-tablename": "ref_schema", "properties": {}},
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_id": {
                            "type": "integer",
                            "x-foreign-key": f"{tablename}.id",
                            "x-dict-ignore": True,
                        }
                    },
                },
            ]
        }
    }
