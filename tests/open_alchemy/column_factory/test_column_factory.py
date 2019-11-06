"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest
import sqlalchemy

from open_alchemy import column_factory


@pytest.mark.prod_env
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


@pytest.mark.parametrize(
    "schemas",
    [
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "table 1",
                "properties": {"id": {"type": "integer"}},
            }
        },
        {
            "RefSchema": {
                "allOf": [
                    {
                        "type": "object",
                        "x-tablename": "table 1",
                        "properties": {"id": {"type": "integer"}},
                    }
                ]
            }
        },
    ],
    ids=["simple", "allOf"],
)
@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_ref(schemas):
    """
    GIVEN schema that references another object schema and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship is returned with the spec.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
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


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_ref_backref():
    """
    GIVEN schema that references another object schema which has x-backref and schemas
    WHEN column_factory is called with the schema and schemas
    THEN relationship with backref is returned.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "x-backref": "backref 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    ([_, (_, relationship)], _) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert relationship.backref == "backref 1"


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_ref_fk_column():
    """
    GIVEN schema that references another object schema which has x-foreign-key-column
        and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference pointing to the foreign key column is returned.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "x-foreign-key-column": "fk_column",
            "properties": {"id": {"type": "integer"}, "fk_column": {"type": "string"}},
        }
    }
    ([(fk_logical_name, fk_column), _], _) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_fk_column"
    assert isinstance(fk_column.type, sqlalchemy.String)
    assert len(fk_column.foreign_keys) == 1


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_ref():
    """
    GIVEN schema with allOf that references another object schema and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship is returned.
    """
    spec = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    (
        [(fk_logical_name, fk_column), (tbl_logical_name, relationship)],
        _,
    ) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_id"
    assert isinstance(fk_column.type, sqlalchemy.Integer)
    assert len(fk_column.foreign_keys) == 1
    assert tbl_logical_name == "column_1"
    assert relationship.argument == "RefSchema"
    assert relationship.backref is None


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_ref_backref():
    """
    GIVEN schema with allOf that references another object schema with backref and
        schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship is returned with a backref.
    """
    spec = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "x-backref": "backref 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    ([_, (_, relationship)], _) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert relationship.backref == "backref 1"


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_ref_fk_column():
    """
    GIVEN schema with allOf that references another object schema with foreign key
        column and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference and relationship is returned pointing to the foreign key
        column.
    """
    spec = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "x-foreign-key-column": "fk_column",
            "properties": {"id": {"type": "integer"}, "fk_column": {"type": "string"}},
        }
    }
    ([(fk_logical_name, fk_column), _], _) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_fk_column"
    assert isinstance(fk_column.type, sqlalchemy.String)


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_backref_ref():
    """
    GIVEN schema with allOf that references another object schema and has x-backref and
        schemas
    WHEN column_factory is called with the schema and schemas
    THEN relationship with backref is returned.
    """
    spec = {
        "allOf": [
            {"$ref": "#/components/schemas/RefSchema"},
            {"x-backref": "backref 1"},
        ]
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    ([_, (_, relationship)], _) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert relationship.backref == "backref 1"


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_fk_column_ref():
    """
    GIVEN schema with allOf that references another object schema and has
        x-foreign-key-column and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key reference to foreign key column is returned.
    """
    spec = {
        "allOf": [
            {"$ref": "#/components/schemas/RefSchema"},
            {"x-foreign-key-column": "fk_column"},
        ]
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "properties": {"id": {"type": "integer"}, "fk_column": {"type": "string"}},
        }
    }
    ([(fk_logical_name, fk_column), _], _) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_fk_column"
    assert isinstance(fk_column.type, sqlalchemy.String)


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_backref_ref_backref():
    """
    GIVEN schema with allOf that references another object schema with backref and has
        x-backref and schemas
    WHEN column_factory is called with the schema and schemas
    THEN backref from allOf is returned.
    """
    spec = {
        "allOf": [
            {"$ref": "#/components/schemas/RefSchema"},
            {"x-backref": "backref 2"},
        ]
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "x-backref": "backref 1",
            "properties": {"id": {"type": "integer"}},
        }
    }
    ([_, (_, relationship)], _) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert relationship.backref == "backref 2"


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_object_all_of_fk_column_ref_fk_column():
    """
    GIVEN schema with allOf that references another object schema with foreign key
        column and has foreign key column and schemas
    WHEN column_factory is called with the schema and schemas
    THEN foreign key column from allOf is returned.
    """
    spec = {
        "allOf": [
            {"$ref": "#/components/schemas/RefSchema"},
            {"x-foreign-key-column": "fk_column_2"},
        ]
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "table 1",
            "x-foreign-key-column": "fk_column_1",
            "properties": {
                "id": {"type": "integer"},
                "fk_column_1": {"type": "string"},
                "fk_column_2": {"type": "boolean"},
            },
        }
    }
    ([(fk_logical_name, fk_column), _], _) = column_factory.column_factory(
        spec=spec, schemas=schemas, logical_name="column_1"
    )

    assert fk_logical_name == "column_1_fk_column_2"
    assert isinstance(fk_column.type, sqlalchemy.Boolean)


@pytest.mark.prod_env
@pytest.mark.column
def test_integration_all_of():
    """
    GIVEN schema with allOf statement
    WHEN column_factory is called with the schema and schemas
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
