"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy import facades
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
            required=True,
            logical_name="name 1",
            model_name="schema",
            model_schema={},
        )


@pytest.mark.column
def test_integration_object_ref():
    """
    GIVEN schema that references another object schema and schemas
    WHEN handle_object is called with the schema and schemas
    THEN foreign key reference and relationship is returned with the spec.
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

    (
        [(fk_logical_name, fk_column), (tbl_logical_name, relationship)],
        returned_schema,
    ) = object_ref.handle_object(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema={"properties": {}},
        model_name="schema",
        required=False,
    )

    assert fk_logical_name == "ref_schema_id"
    assert isinstance(fk_column.type, facades.sqlalchemy.column.Integer)
    assert fk_column.nullable is True
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == logical_name
    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert relationship.uselist is None
    assert returned_schema == {"type": "object", "x-de-$ref": "RefSchema"}


@pytest.mark.column
def test_integration_object_ref_required():
    """
    GIVEN schema that is required and references another object schema and schemas
    WHEN handle_object is called with the schema and schemas
    THEN foreign key which is not nullable is returned.
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

    ([(_, fk_column), _], _) = object_ref.handle_object(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema={"properties": {}},
        model_name="schema",
        required=True,
    )

    assert fk_column.nullable is False


@pytest.mark.column
def test_integration_object_ref_nullable():
    """
    GIVEN schema that is not nullable and references another object schema and schemas
    WHEN handle_object is called with the schema and schemas
    THEN foreign key which is not nullable is returned.
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

    ([(_, fk_column), _], returned_schema) = object_ref.handle_object(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema={"properties": {}},
        model_name="schema",
        required=None,
    )

    assert fk_column.nullable is False
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
    model_schema = {"properties": {}}
    model_name = "Schema"

    ([_, (_, relationship)], _) = object_ref.handle_object(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
        model_name=model_name,
        required=False,
    )

    assert relationship.backref == ("schema", {"uselist": None})
    assert schemas == {
        "RefSchema": {
            "allOf": [
                {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {"id": {"type": "integer"}},
                },
                {
                    "type": "object",
                    "x-backrefs": {
                        "schema": {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": model_name},
                        }
                    },
                },
            ]
        }
    }


@pytest.mark.column
def test_fk_def():
    """
    GIVEN schema that references another object schema which already has the foreign
        key defined and schemas
    WHEN handle_object is called with the schema and schemas
    THEN no foreign key column is returned.
    """
    model_schema = {
        "properties": {
            "ref_schema_id": {"type": "integer", "x-foreign-key": "ref_schema.id"}
        }
    }
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    logical_name = "ref_schema"

    ([(tbl_logical_name, relationship)], _) = object_ref.handle_object(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
        model_name="model",
        required=None,
    )

    assert tbl_logical_name == logical_name
    assert relationship.argument == "RefSchema"
