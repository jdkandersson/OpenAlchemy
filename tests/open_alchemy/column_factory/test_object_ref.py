"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy.column_factory import object_ref


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
        object_ref.handle_object(
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
        object_ref._handle_object_reference(spec={"properties": {"id": {}}}, schemas={})


@pytest.mark.column
def test_handle_object_reference_no_properties():
    """
    GIVEN object schema without properties key
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        object_ref._handle_object_reference(spec={"x-tablename": "table 1"}, schemas={})


@pytest.mark.column
def test_handle_object_reference_id_missing():
    """
    GIVEN object schema without id in properties
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        object_ref._handle_object_reference(
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
        object_ref._handle_object_reference(
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
        object_ref._handle_object_reference(
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

    return_value = object_ref._handle_object_reference(spec=spec, schemas=schemas)

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

    return_value = object_ref._handle_object_reference(
        spec=spec, schemas=schemas, fk_column="fk"
    )

    assert return_value == {"type": "fkType", "x-foreign-key": "table 1.fk"}
