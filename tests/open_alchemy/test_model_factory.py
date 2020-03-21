"""Input validation tests."""
# Disable protected access for testing.
# pylint: disable=protected-access

import copy
from unittest import mock

import pytest
from sqlalchemy import schema

from open_alchemy import exceptions
from open_alchemy import model_factory


@pytest.mark.model
def test_missing_schema():
    """
    GIVEN schemas and name that is not in schemas
    WHEN model_factory is called
    THEN SchemaNotFoundError is raised.
    """
    with pytest.raises(exceptions.SchemaNotFoundError):
        model_factory.model_factory(name="Missing", base=None, schemas={})


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


@pytest.mark.model
def test_tablename_none():
    """
    GIVEN schemas with schema that has None for the tablename
    WHEN model_factory is called with the name of the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        model_factory.model_factory(
            name="SingleProperty",
            base=mock.MagicMock,
            schemas={
                "SingleProperty": {
                    "x-tablename": None,
                    "type": "object",
                    "properties": {"property_1": {"type": "integer"}},
                }
            },
        )


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


@pytest.mark.model
def test_tablename():
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
    model_schema = {
        "x-tablename": "table 1",
        "type": "object",
        "properties": {"id": {"type": "integer"}},
    }
    model_name = "SingleProperty"
    schemas = {model_name: model_schema}
    model_factory.model_factory(
        name=model_name, base=mock.MagicMock, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        spec={"type": "integer"},
        schemas=schemas,
        logical_name="id",
        required=None,
        model_name=model_name,
        model_schema=model_schema,
    )


@pytest.mark.model
def test_single_property_not_required(mocked_column_factory: mock.MagicMock):
    """
    GIVEN mocked column_factory and schemas with schema that has single item properties
        key and a required key without the key in properties
    WHEN model_factory is called with the name of the schema
    THEN column_factory is called with required reset.
    """
    model_schema = {
        "x-tablename": "table 1",
        "type": "object",
        "properties": {"id": {"type": "integer"}},
        "required": [],
    }
    model_name = "SingleProperty"
    schemas = {model_name: model_schema}
    model_factory.model_factory(
        name=model_name, base=mock.MagicMock, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        spec={"type": "integer"},
        schemas=schemas,
        logical_name="id",
        required=False,
        model_name=model_name,
        model_schema=model_schema,
    )


@pytest.mark.model
def test_single_property_required(mocked_column_factory: mock.MagicMock):
    """
    GIVEN mocked column_factory and schemas with schema that has single item properties
        key and a required key with the key in properties
    WHEN model_factory is called with the name of the schema
    THEN column_factory is called with required reset.
    """
    model_schema = {
        "x-tablename": "table 1",
        "type": "object",
        "properties": {"id": {"type": "integer"}},
        "required": ["id"],
    }
    model_name = "SingleProperty"
    schemas = {model_name: model_schema}
    model_factory.model_factory(
        name=model_name, base=mock.MagicMock, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        spec={"type": "integer"},
        schemas=schemas,
        logical_name="id",
        required=True,
        model_name=model_name,
        model_schema=model_schema,
    )


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


@pytest.mark.parametrize(
    "schemas, expected_schema",
    [
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {
                        "property_1": {"type": "integer", "x-dict-ignore": True}
                    },
                }
            },
            {"type": "object", "properties": {}},
        ),
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {
                        "property_1": {"type": "integer", "x-dict-ignore": False}
                    },
                }
            },
            {"type": "object", "properties": {"property_1": {"type": "integer"}}},
        ),
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {"property_1": {"type": "integer"}},
                }
            },
            {"type": "object", "properties": {"property_1": {"type": "integer"}}},
        ),
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {"property_1": {"type": "integer"}},
                    "required": ["property_1"],
                }
            },
            {
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
                "required": ["property_1"],
            },
        ),
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {"property_1": {"type": "integer"}},
                    "x-backrefs": {
                        "ref_schema": {"type": "object", "x-de-$ref": "RefSchema"}
                    },
                }
            },
            {
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
                "x-backrefs": {
                    "ref_schema": {"type": "object", "x-de-$ref": "RefSchema"}
                },
            },
        ),
        (
            {
                "RefSchema": {"type": "integer"},
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {
                        "property_1": {"$ref": "#/components/schemas/RefSchema"}
                    },
                },
            },
            {"type": "object", "properties": {"property_1": {"type": "integer"}}},
        ),
        (
            {
                "RefSchema": {
                    "x-tablename": "table 2",
                    "type": "object",
                    "properties": {"id": {"type": "integer"}},
                },
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {
                        "property_1": {"$ref": "#/components/schemas/RefSchema"}
                    },
                },
            },
            {
                "type": "object",
                "properties": {
                    "property_1": {"type": "object", "x-de-$ref": "RefSchema"}
                },
            },
        ),
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {"property_1": {"allOf": [{"type": "integer"}]}},
                }
            },
            {"type": "object", "properties": {"property_1": {"type": "integer"}}},
        ),
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {"property_1": {"type": "integer"}},
                    "description": "",
                }
            },
            {
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
                "description": "",
            },
        ),
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {"property_1": {"type": "integer"}},
                    "description": "description 1",
                }
            },
            {
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
                "description": "description 1",
            },
        ),
        (
            {
                "Schema": {
                    "x-tablename": "table 1",
                    "type": "object",
                    "properties": {
                        "property_1": {"type": "integer"},
                        "property_2": {"type": "string"},
                    },
                }
            },
            {
                "type": "object",
                "properties": {
                    "property_1": {"type": "integer"},
                    "property_2": {"type": "string"},
                },
            },
        ),
    ],
    ids=[
        "single x-dict-ignore true",
        "single x-dict-ignore false",
        "single no required, backrefs",
        "single required",
        "single x-backrefs",
        "single ref",
        "single ref object",
        "single allOf",
        "single description empty",
        "single description",
        "multiple properties",
    ],
)
@pytest.mark.model
def test_schema(schemas, expected_schema):
    """
    GIVEN schemas and expected schema
    WHEN model_factory is called with the schemas and the name of a schema
    THEN a model with _schema set to the expected schema is returned.
    """
    model = model_factory.model_factory(
        name="Schema", base=mock.MagicMock, schemas=schemas
    )

    assert model._schema == expected_schema


@pytest.mark.model
def test_schema_relationship_invalid():
    """
    GIVEN schema with x-backrefs with invalid schema
    WHEN model_factory is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    schemas = {
        "Schema": {
            "x-tablename": "table 1",
            "type": "object",
            "properties": {"property_1": {"type": "integer"}},
            "x-backrefs": {"ref_schema": "RefSchema"},
        }
    }

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        model_factory.model_factory(name="Schema", base=mock.MagicMock, schemas=schemas)


@pytest.mark.model
def test_table_args_unique():
    """
    GIVEN schemas with schema that has a unique constraint
    WHEN model_factory is called with the name of the schema
    THEN a model with a unique constraint is returned.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        base=mock.MagicMock,
        schemas={
            "SingleProperty": {
                "x-tablename": "table 1",
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
                "x-composite-unique": ["property_1"],
            }
        },
    )

    (unique,) = model.__table_args__
    assert isinstance(unique, schema.UniqueConstraint)


@pytest.mark.model
def test_table_args_index():
    """
    GIVEN schemas with schema that has a composite index
    WHEN model_factory is called with the name of the schema
    THEN a model with a composite index is returned.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        base=mock.MagicMock,
        schemas={
            "SingleProperty": {
                "x-tablename": "table 1",
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
                "x-composite-index": ["property_1"],
            }
        },
    )

    (index,) = model.__table_args__
    assert isinstance(index, schema.Index)
