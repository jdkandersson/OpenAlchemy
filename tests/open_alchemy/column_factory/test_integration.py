"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest

from open_alchemy import column_factory
from open_alchemy import facades


@pytest.mark.column
def test_integration():
    """
    GIVEN schema
    WHEN column_factory is called with the schema
    THEN SQLAlchemy boolean column is returned in a dictionary with logical name and
        spec.
    """
    spec = {"type": "boolean"}
    schemas = {}
    ([(logical_name, column)], spec) = column_factory.column_factory(
        spec=spec,
        schemas=schemas,
        logical_name="column_1",
        model_schema={},
        model_name="schema",
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, facades.sqlalchemy.column.Boolean)
    assert spec == {"type": "boolean"}


@pytest.mark.column
def test_integration_all_of():
    """
    GIVEN schema with allOf statement
    WHEN column_factory is called with the schema
    THEN SQLAlchemy boolean column is returned in a dictionary with logical name and
        spec.
    """
    spec = {"allOf": [{"type": "boolean"}]}
    schemas = {}
    ([(logical_name, column)], spec) = column_factory.column_factory(
        spec=spec,
        schemas=schemas,
        logical_name="column_1",
        model_schema={},
        model_name="schema",
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, facades.sqlalchemy.column.Boolean)
    assert spec == {"type": "boolean"}


@pytest.mark.column
def test_integration_ref():
    """
    GIVEN schema that references another schema and schemas
    WHEN column_factory is called with the schema and schemas
    THEN SQLAlchemy boolean column is returned in a dictionary with logical name and
        the spec.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {"RefSchema": {"type": "boolean"}}
    ([(logical_name, column)], spec) = column_factory.column_factory(
        spec=spec,
        schemas=schemas,
        logical_name="column_1",
        model_schema={},
        model_name="schema",
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, facades.sqlalchemy.column.Boolean)
    assert spec == {"type": "boolean"}


@pytest.mark.column
def test_integration_object_ref():
    """
    GIVEN schema that references another object schema and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship is returned with the spec.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
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
        spec,
    ) = column_factory.column_factory(
        spec=spec,
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
    assert spec == {"type": "object", "x-de-$ref": "RefSchema"}


@pytest.mark.column
def test_integration_array_ref():
    """
    GIVEN schema that references another object schema from an array and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference  is added to the referenced schema and relationship is
        returned with the spec.
    """
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
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

    ([(tbl_logical_name, relationship)], spec) = column_factory.column_factory(
        spec=spec,
        schemas=schemas,
        logical_name=logical_name,
        model_schema=model_schema,
        model_name="model",
    )

    assert tbl_logical_name == logical_name
    assert relationship.argument == "RefSchema"
    assert spec == {
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
