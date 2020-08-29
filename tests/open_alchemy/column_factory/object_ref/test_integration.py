"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy.column_factory import object_ref


@pytest.mark.parametrize(
    "schema, schemas",
    [
        ({"type": "object"}, {}),
        ({"allOf": [{"type": "object"}]}, {}),
        (
            {"$ref": "#/components/schemas/Schema"},
            {
                "Schema": {
                    "type": "object",
                    "x-tablename": "table",
                    "x-secondary": "secondary",
                }
            },
        ),
    ],
    ids=["object", "allOf with object", "secondary defined"],
)
@pytest.mark.column
def test_handle_object_error(schema, schemas):
    """
    GIVEN schema
    WHEN handle_object is called with the schema
    THEN MalformedRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedRelationshipError):
        object_ref.handle_object(
            schema=schema,
            schemas=schemas,
            logical_name="name 1",
        )


@pytest.mark.column
def test_integration_object_ref():
    """
    GIVEN schema that references another object schema and schemas
    WHEN handle_object is called with the schema and schemas
    THEN relationship is returned with the spec.
    """
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    logical_name = "ref_schema"

    ([(tbl_logical_name, relationship)], returned_schema,) = object_ref.handle_object(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
    )

    assert tbl_logical_name == logical_name
    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert relationship.uselist is None
    assert returned_schema == {"type": "object", "x-de-$ref": "RefSchema"}


@pytest.mark.column
def test_integration_object_ref_nullable():
    """
    GIVEN schema that is not nullable and references another object schema and schemas
    WHEN handle_object is called with the schema and schemas
    THEN schema which is not nullable is returned.
    """
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {"id": {"type": "integer"}},
            "nullable": False,
        }
    }
    logical_name = "ref_schema"

    (_, returned_schema) = object_ref.handle_object(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
    )

    assert returned_schema == {
        "type": "object",
        "x-de-$ref": "RefSchema",
        "nullable": False,
    }


@pytest.mark.column
def test_integration_object_ref_backref():
    """
    GIVEN schema that references another object schema with a back reference and schemas
    WHEN handle_object is called with the schema and schemas
    THEN the a relationship with a back reference is returned and the back reference is
        recorded on the referenced schema.
    """
    schema = {
        "allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"x-backref": "schema"}]
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    logical_name = "ref_schema"

    ([(_, relationship)], _) = object_ref.handle_object(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
    )

    assert relationship.backref == ("schema", {"uselist": None})
    assert schemas == {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
