"""Input validation tests."""
# Disable protected access for testing.
# pylint: disable=protected-access

import copy
from unittest import mock

import pytest

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import model_factory


@pytest.mark.prod_env
@pytest.mark.model
def test_missing_schema():
    """
    GIVEN schemas and name that is not in schemas
    WHEN model_factory is called
    THEN SchemaNotFoundError is raised.
    """
    with pytest.raises(exceptions.SchemaNotFoundError):
        model_factory.model_factory(name="Missing", base=None, schemas={})


@pytest.mark.prod_env
@pytest.mark.model
def test_missing_tablename():
    """
    GIVEN schemas and name that refers to a schema without the x-tablename key
    WHEN model_factory is called
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        model_factory.model_factory(
            name="MissingTablename", base=None, schemas={"MissingTablename": {}}
        )


@pytest.mark.prod_env
@pytest.mark.model
def test_not_object():
    """
    GIVEN schemas with schema that is not an object
    WHEN model_factory is called with the name of the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        model_factory.model_factory(
            name="NotObject",
            base=None,
            schemas={"NotObject": {"x-tablename": "table 1", "type": "not_object"}},
        )


@pytest.mark.prod_env
@pytest.mark.model
def test_properties_missing():
    """
    GIVEN schemas with schema that does not have the properties key
    WHEN model_factory is called with the name of the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        model_factory.model_factory(
            name="MissingProperty",
            base=None,
            schemas={"MissingProperty": {"x-tablename": "table 1", "type": "object"}},
        )


@pytest.mark.prod_env
@pytest.mark.model
def test_properties_empty():
    """
    GIVEN schemas with schema that has empty properties key
    WHEN model_factory is called with the name of the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        model_factory.model_factory(
            name="EmptyProperty",
            base=None,
            schemas={
                "EmptyProperty": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {},
                }
            },
        )


@pytest.mark.prod_env
@pytest.mark.model
def test_single_property():
    """
    GIVEN schemas with schema that has single item properties key
    WHEN model_factory is called with the name of the schema
    THEN a model with the property is returned.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        base=mock.MagicMock,
        schemas={
            "SingleProperty": {
                "x-tablename": "table 1",
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
            }
        },
    )

    assert hasattr(model, "property_1")


@pytest.mark.prod_env
@pytest.mark.model
def test_multiple_property():
    """
    GIVEN schemas with schema that has multiple item properties key
    WHEN model_factory is called with the name of the schema
    THEN a model with the properties is returned.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        base=mock.MagicMock,
        schemas={
            "SingleProperty": {
                "x-tablename": "table 1",
                "type": "object",
                "properties": {
                    "property_1": {"type": "integer"},
                    "property_2": {"type": "integer"},
                },
            }
        },
    )

    assert hasattr(model, "property_1")
    assert hasattr(model, "property_2")


@pytest.mark.prod_env
@pytest.mark.model
def test_single_tablename():
    """
    GIVEN schemas with schema
    WHEN model_factory is called with the name of the schema
    THEN a model where __tablename__ has been set to the x-tablename value.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        base=mock.MagicMock,
        schemas={
            "SingleProperty": {
                "x-tablename": "table 1",
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
            }
        },
    )

    assert model.__tablename__ == "table 1"


@pytest.mark.model
def test_single_property_required_missing(mocked_column_factory: mock.MagicMock):
    """
    GIVEN mocked column_factory and schemas with schema that has single item properties
        key and does not have the required key
    WHEN model_factory is called with the name of the schema
    THEN column_factory is called with required as None.
    """
    schemas = {
        "SingleProperty": {
            "x-tablename": "table 1",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        }
    }
    model_factory.model_factory(
        name="SingleProperty", base=mock.MagicMock, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        spec={"type": "integer"}, schemas=schemas, logical_name="id", required=None
    )


@pytest.mark.model
def test_single_property_not_required(mocked_column_factory: mock.MagicMock):
    """
    GIVEN mocked column_factory and schemas with schema that has single item properties
        key and a required key without the key in properties
    WHEN model_factory is called with the name of the schema
    THEN column_factory is called with required reset.
    """
    schemas = {
        "SingleProperty": {
            "x-tablename": "table 1",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
            "required": [],
        }
    }
    model_factory.model_factory(
        name="SingleProperty", base=mock.MagicMock, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        spec={"type": "integer"}, schemas=schemas, logical_name="id", required=False
    )


@pytest.mark.model
def test_single_property_required(mocked_column_factory: mock.MagicMock):
    """
    GIVEN mocked column_factory and schemas with schema that has single item properties
        key and a required key with the key in properties
    WHEN model_factory is called with the name of the schema
    THEN column_factory is called with required reset.
    """
    schemas = {
        "SingleProperty": {
            "x-tablename": "table 1",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
            "required": ["id"],
        }
    }
    model_factory.model_factory(
        name="SingleProperty", base=mock.MagicMock, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        spec={"type": "integer"}, schemas=schemas, logical_name="id", required=True
    )


@pytest.mark.prod_env
@pytest.mark.model
def test_ref():
    """
    GIVEN schemas with schema that has $ref and the referenced schema
    WHEN model_factory is called with the name of the schema
    THEN a model with the property and tablename is returned.
    """
    model = model_factory.model_factory(
        name="Schema",
        base=mock.MagicMock,
        schemas={
            "Schema": {"$ref": "#/components/schemas/RefSchema"},
            "RefSchema": {
                "x-tablename": "table 1",
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
            },
        },
    )

    assert hasattr(model, "property_1")
    assert model.__tablename__ == "table 1"


@pytest.mark.prod_env
@pytest.mark.model
def test_all_of():
    """
    GIVEN schemas with schema that has allOf and the referenced schema
    WHEN model_factory is called with the name of the schema
    THEN a model with the property and tablename is returned.
    """
    model = model_factory.model_factory(
        name="Schema",
        base=mock.MagicMock,
        schemas={
            "Schema": {
                "allOf": [
                    {
                        "x-tablename": "table 1",
                        "type": "object",
                        "properties": {"property_1": {"type": "integer"}},
                    }
                ]
            }
        },
    )

    assert hasattr(model, "property_1")
    assert model.__tablename__ == "table 1"
