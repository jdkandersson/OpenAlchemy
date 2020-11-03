"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest

from open_alchemy import column_factory
from open_alchemy import facades


@pytest.mark.parametrize(
    "schema, expected_schema",
    [
        pytest.param({"type": "boolean"}, {"type": "boolean"}, id="any basic type"),
        pytest.param(
            {"type": "boolean", "readOnly": True},
            {"type": "boolean", "readOnly": True},
            id="any basic type with readOnly",
        ),
    ],
)
@pytest.mark.column
def test_integration_simple(schema, expected_schema):
    """
    GIVEN schema
    WHEN column_factory is called with the schema
    THEN a SQLAlchemy boolean column is returned in a tuple with logical name and
        schema.
    """
    schemas = {}
    model_schema = {"type": "object"}
    ([(logical_name, column)], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name="column_1",
        model_schema=model_schema,
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, facades.sqlalchemy.types.Boolean)
    assert returned_schema == expected_schema


@pytest.mark.parametrize(
    "required, expected_nullable",
    [
        pytest.param(None, True, id="None"),
        pytest.param(False, True, id="False"),
        pytest.param(True, False, id="True"),
    ],
)
@pytest.mark.column
def test_integration_simple_required(required, expected_nullable):
    """
    GIVEN required and expected nullable
    WHEN column_factory is called with the required
    THEN a SQLAlchemy boolean column is returned with the expected nullable value.
    """
    schema = {"type": "boolean"}
    schemas = {}
    model_schema = {"type": "object"}
    ([(_, column)], _) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name="column_1",
        model_schema=model_schema,
        required=required,
    )

    assert column.nullable == expected_nullable


@pytest.mark.parametrize(
    "schema, expected_schema",
    [
        pytest.param(
            {"type": "boolean", "x-json": True},
            {"type": "boolean", "x-json": True},
            id="simple",
        ),
        pytest.param(
            {
                "type": "object",
                "x-json": True,
                "properties": {"key": {"type": "integer"}},
            },
            {
                "type": "object",
                "x-json": True,
                "properties": {"key": {"type": "integer"}},
            },
            id="object",
        ),
        pytest.param(
            {"type": "array", "x-json": True},
            {"type": "array", "x-json": True},
            id="array",
        ),
    ],
)
@pytest.mark.column
def test_integration_simple_json(schema, expected_schema):
    """
    GIVEN JSON schema and expected schema
    WHEN column_factory is called with the schema
    THEN a SQLALchemy JSON column and the expected schema are returned.
    """
    schemas = {}
    model_schema = {"type": "object"}
    ([(logical_name, column)], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name="column_1",
        model_schema=model_schema,
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, facades.sqlalchemy.types.JSON)
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
    model_schema = {"type": "object"}
    ([(_, column)], _) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        model_schema=model_schema,
        logical_name="column_1",
    )

    assert column.doc == "doc 1"


@pytest.mark.column
def test_integration_relationship_many_to_one():
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
    model_schema = {"type": "object"}
    logical_name = "ref_schema"

    (
        [(tbl_logical_name, relationship)],
        returned_schema,
    ) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
    )

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
    model_schema = {"type": "object"}
    logical_name = "ref_schema"

    ([], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
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
    THEN relationship is returned with the schema.
    """
    schema = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    model_schema = {"type": "object", "x-tablename": "schema"}
    logical_name = "ref_schema"

    (
        [(tbl_logical_name, relationship)],
        returned_schema,
    ) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
    )

    assert tbl_logical_name == logical_name
    assert relationship.argument == "RefSchema"
    assert returned_schema == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }
    assert schemas == {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        },
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
    model_schema = {"type": "object", "x-tablename": "schema"}
    logical_name = "ref_schema"

    ([], returned_schema) = column_factory.column_factory(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
    )

    assert returned_schema == {
        "type": "array",
        "items": {"type": "object", "properties": {"id": {"type": "integer"}}},
        "readOnly": True,
    }
