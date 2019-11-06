"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest
import sqlalchemy

from open_alchemy import column_factory
from open_alchemy import exceptions


@pytest.mark.parametrize(
    "spec",
    [
        {"type": "object"},
        {"allOf": [{"type": "object"}]},
        {"allOf": [{"$ref": "ref 1"}, {"$ref": "ref 2"}]},
        {
            "allOf": [
                {"$ref": "ref 1"},
                {"x-backref": "backref 1"},
                {"x-backref": "backref 2"},
            ]
        },
        {
            "allOf": [
                {"$ref": "ref 1"},
                {"x-foreign-key-column": "column 1"},
                {"x-foreign-key-column": "column 2"},
            ]
        },
    ],
    ids=[
        "object",
        "allOf with object",
        "allOf with multiple ref",
        "allOf with multiple x-backref",
        "allOf with multiple x-foreign-key-column",
    ],
)
@pytest.mark.column
def test_handle_object_error(spec):
    """
    GIVEN spec
    WHEN handle_object is called with the spec
    THEN MalformedManyToOneRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedManyToOneRelationshipError):
        column_factory.object_ref.handle_object(
            spec=spec, schemas={}, required=True, logical_name="name 1"
        )


@pytest.mark.column
def test_handle_object_reference_no_tablename():
    """
    GIVEN object schema without x-tablename key
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory.object_ref._handle_object_reference(
            spec={"properties": {"id": {}}}, schemas={}
        )


@pytest.mark.column
def test_handle_object_reference_no_properties():
    """
    GIVEN object schema without properties key
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory.object_ref._handle_object_reference(
            spec={"x-tablename": "table 1"}, schemas={}
        )


@pytest.mark.column
def test_handle_object_reference_id_missing():
    """
    GIVEN object schema without id in properties
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory.object_ref._handle_object_reference(
            spec={"x-tablename": "table 1", "properties": {}}, schemas={}
        )


@pytest.mark.column
def test_handle_object_reference_name_missing():
    """
    GIVEN foreign key argument and object schema without foreign key property
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory.object_ref._handle_object_reference(
            spec={"x-tablename": "table 1", "properties": {"id": {"type": "integer"}}},
            schemas={},
            fk_column="column_1",
        )


@pytest.mark.column
def test_handle_object_reference_id_no_type():
    """
    GIVEN object schema with id but no type for id
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        column_factory.object_ref._handle_object_reference(
            spec={"x-tablename": "table 1", "properties": {"id": {}}}, schemas={}
        )


@pytest.mark.column
def test_handle_object_reference_return():
    """
    GIVEN object schema with x-tablename and id property with a type
    WHEN _handle_object_reference is called with the schema
    THEN a schema with the type of the id property and x-foreign-key property.
    """
    spec = {"x-tablename": "table 1", "properties": {"id": {"type": "idType"}}}
    schemas = {}

    return_value = column_factory.object_ref._handle_object_reference(
        spec=spec, schemas=schemas
    )

    assert return_value == {"type": "idType", "x-foreign-key": "table 1.id"}


@pytest.mark.column
def test_handle_object_reference_fk_return():
    """
    GIVEN foreign key column and object schema with x-tablename and id and foreign key
        property with a type
    WHEN _handle_object_reference is called with the schema
    THEN a schema with the type of the foreign key property and x-foreign-key property.
    """
    spec = {
        "x-tablename": "table 1",
        "properties": {"id": {"type": "idType"}, "fk": {"type": "fkType"}},
    }
    schemas = {}

    return_value = column_factory.object_ref._handle_object_reference(
        spec=spec, schemas=schemas, fk_column="fk"
    )

    assert return_value == {"type": "fkType", "x-foreign-key": "table 1.fk"}


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
