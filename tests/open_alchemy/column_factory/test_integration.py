"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest

from open_alchemy import column_factory
from open_alchemy import facades


@pytest.mark.parametrize(
    "schema, expected_schema",
    [
        ({"type": "boolean"}, {"type": "boolean"}),
        ({"type": "boolean", "readOnly": True}, {"type": "boolean", "readOnly": True}),
    ],
    ids=["any basic type", "any basic type with readOnly"],
)
@pytest.mark.column
def test_integration_simple(schema, expected_schema):
    """
    GIVEN schema
    WHEN column_factory is called with the schema
    THEN SQLAlchemy boolean column is returned in a dictionary with logical name and
        schema.
    """
    schemas = {}
    ([(logical_name, column)], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name="column_1",
        model_schema={},
        model_name="schema",
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, facades.sqlalchemy.column.Boolean)
    assert returned_schema == expected_schema


@pytest.mark.column
def test_integration_kwargs():
    """
    GIVEN schema with kwargs
    WHEN column_factory is called with the schema
    THEN SQLAlchemy column is constructed with the kwargs.
    """
    schema = {"type": "boolean", "x-kwargs": {"doc": "doc 1"}}
    schemas = {}
    ([(_, column)], _) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name="column_1",
        model_schema={},
        model_name="schema",
    )

    assert column.doc == "doc 1"


@pytest.mark.column
def test_integration_all_of():
    """
    GIVEN schema with allOf statement
    WHEN column_factory is called with the schema
    THEN SQLAlchemy boolean column is returned in a dictionary with logical name and
        schema.
    """
    schema = {"allOf": [{"type": "boolean"}]}
    schemas = {}
    ([(logical_name, column)], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name="column_1",
        model_schema={},
        model_name="schema",
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, facades.sqlalchemy.column.Boolean)
    assert returned_schema == {"type": "boolean"}


@pytest.mark.column
def test_integration_ref():
    """
    GIVEN schema that references another schema and schemas
    WHEN column_factory is called with the schema and schemas
    THEN SQLAlchemy boolean column is returned in a dictionary with logical name and
        the schema.
    """
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {"RefSchema": {"type": "boolean"}}
    ([(logical_name, column)], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name="column_1",
        model_schema={},
        model_name="schema",
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, facades.sqlalchemy.column.Boolean)
    assert returned_schema == {"type": "boolean"}


@pytest.mark.column
def test_integration_object_ref():
    """
    GIVEN schema that references another object schema and schemas
    WHEN column_factory is called with the schema and schemas
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
    ) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema={"properties": {}},
        model_name="schema",
    )

    assert fk_logical_name == "ref_schema_id"
    assert isinstance(fk_column.type, facades.sqlalchemy.column.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == logical_name
    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert relationship.uselist is None
    assert returned_schema == {"type": "object", "x-de-$ref": "RefSchema"}


@pytest.mark.column
def test_integration_object_ref_read_only():
    """
    GIVEN schema that references another object schema and is readOnly and schemas
    WHEN column_factory is called with the schema and schemas
    THEN no columns and the schema is returned.
    """
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {"id": {"type": "integer"}},
            "readOnly": True,
        }
    }
    logical_name = "ref_schema"

    ([], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema={"properties": {}},
        model_name="schema",
    )

    assert returned_schema == {
        "type": "object",
        "properties": {"id": {"type": "integer"}},
        "readOnly": True,
    }


@pytest.mark.column
def test_integration_array_ref():
    """
    GIVEN schema that references another object schema from an array and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference  is added to the referenced schema and relationship is
        returned with the schema.
    """
    schema = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }
    logical_name = "ref_schema"

    (
        [(tbl_logical_name, relationship)],
        returned_schema,
    ) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
        model_name="model",
    )

    assert tbl_logical_name == logical_name
    assert relationship.argument == "RefSchema"
    assert returned_schema == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }
    assert schemas == {
        "RefSchema": {
            "allOf": [
                {
                    "type": "object",
                    "x-tablename": "table 1",
                    "properties": {"id": {"type": "integer"}},
                },
                {
                    "type": "object",
                    "properties": {
                        "schema_id": {
                            "type": "integer",
                            "x-foreign-key": "schema.id",
                            "x-dict-ignore": True,
                        }
                    },
                },
            ]
        }
    }


@pytest.mark.column
def test_integration_array_ref_read_only():
    """
    GIVEN schema that references another object schema from an array that is read only
        and schemas
    WHEN column_factory is called with the schema and schemas
    THEN no columns and the schema is returned.
    """
    schema = {
        "type": "array",
        "items": {"$ref": "#/components/schemas/RefSchema"},
        "readOnly": True,
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }
    logical_name = "ref_schema"

    ([], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
        model_name="model",
    )

    assert returned_schema == {
        "type": "array",
        "items": {"type": "object", "properties": {"id": {"type": "integer"}}},
        "readOnly": True,
    }
