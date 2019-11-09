"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest
import sqlalchemy

from open_alchemy import column_factory


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
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, sqlalchemy.Boolean)
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
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, sqlalchemy.Boolean)
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
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert logical_name == "column_1"
    assert isinstance(column.type, sqlalchemy.Boolean)
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
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    (
        [(fk_logical_name, fk_column), (tbl_logical_name, relationship)],
        spec,
    ) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_id"
    assert isinstance(fk_column.type, sqlalchemy.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == "column_1"
    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert spec == {"type": "object", "x-de-$ref": "RefSchema"}


@pytest.mark.column
def test_integration_object_ref_backref():
    """
    GIVEN schema that references another object schema with a backref and schemas
    WHEN column_factory is called with the schema and schemas
    THEN relationship with backref is returned with the spec.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
            "x-backref": "ref_schemas",
        }
    }
    ([_, (_, relationship)], spec) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert relationship.backref == "ref_schemas"
