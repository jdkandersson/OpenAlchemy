"""Input validation tests."""
# Disable protected access for testing.
# pylint: disable=protected-access,no-member

import copy
import importlib
from unittest import mock

import pytest
from sqlalchemy import schema as sql_schema

from open_alchemy import exceptions
from open_alchemy import model_factory
from open_alchemy.facades import sqlalchemy


def _mock_get_base(**_):
    """Mock get_base function."""
    return mock.MagicMock


@pytest.mark.model
def test_single_property():
    """
    GIVEN schemas with schema that has single item properties key
    WHEN model_factory is called with the name of the schema
    THEN a model with the property is returned.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        get_base=_mock_get_base,
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
        get_base=_mock_get_base,
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
        get_base=_mock_get_base,
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
        name=model_name, get_base=_mock_get_base, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        schema={"type": "integer"},
        schemas=schemas,
        logical_name="id",
        required=None,
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
        name=model_name, get_base=_mock_get_base, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        schema={"type": "integer"},
        schemas=schemas,
        logical_name="id",
        required=False,
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
        name=model_name, get_base=_mock_get_base, schemas=copy.deepcopy(schemas)
    )

    mocked_column_factory.assert_called_once_with(
        schema={"type": "integer"},
        schemas=schemas,
        logical_name="id",
        required=True,
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
        get_base=_mock_get_base,
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
        get_base=_mock_get_base,
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


@pytest.mark.model
def test_inherits():
    """
    GIVEN schemas with schema that inherits
    WHEN model_factory is called with the name of the schema
    THEN a model which inherits from the parent and with only the child properties
        defined is returned.
    """
    model = model_factory.model_factory(
        name="Child",
        get_base=_mock_get_base,
        schemas={
            "Child": {
                "allOf": [
                    {
                        "x-inherits": True,
                        "type": "object",
                        "properties": {"property_2": {"type": "integer"}},
                    },
                    {"$ref": "#/components/schemas/Parent"},
                ]
            },
            "Parent": {
                "x-tablename": "parent",
                "type": "object",
                "properties": {"property_1": {"type": "string"}},
            },
        },
    )

    assert not hasattr(model, "property_1")
    assert hasattr(model, "property_2")
    assert getattr(model, "__tablename__", None) is None


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
        (
            {
                "Schema": {
                    "allOf": [
                        {
                            "x-inherits": True,
                            "type": "object",
                            "properties": {"property_2": {"type": "string"}},
                        },
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
                "Parent": {
                    "x-tablename": "parent",
                    "type": "object",
                    "properties": {"property_1": {"type": "integer"}},
                },
            },
            {
                "type": "object",
                "properties": {"property_2": {"type": "string"}},
                "x-inherits": "Parent",
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
        "x-inherits",
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
        name="Schema", get_base=_mock_get_base, schemas=schemas
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
        model_factory.model_factory(
            name="Schema", get_base=_mock_get_base, schemas=schemas
        )


@pytest.mark.model
def test_table_args_unique():
    """
    GIVEN schemas with schema that has a unique constraint
    WHEN model_factory is called with the name of the schema
    THEN a model with a unique constraint is returned.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        get_base=_mock_get_base,
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
    assert isinstance(unique, sql_schema.UniqueConstraint)


@pytest.mark.model
def test_table_args_index():
    """
    GIVEN schemas with schema that has a composite index
    WHEN model_factory is called with the name of the schema
    THEN a model with a composite index is returned.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        get_base=_mock_get_base,
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
    assert isinstance(index, sql_schema.Index)


@pytest.mark.model
def test_mixin(monkeypatch):
    """
    GIVEN schemas with schema that has a mixin
    WHEN model_factory is called with the name of the schema
    THEN a model with the property is returned.
    """
    # Define mixin
    mock_import_module = mock.MagicMock()
    mixin_class = type(
        "Mixin1",
        (),
        {
            "property_2": sqlalchemy.column.Column(sqlalchemy.column.Integer),
            "__abstract__": True,
        },
    )
    mock_import_module.return_value.Mixin1 = mixin_class
    monkeypatch.setattr(importlib, "import_module", mock_import_module)

    model = model_factory.model_factory(
        name="SingleProperty",
        get_base=_mock_get_base,
        schemas={
            "SingleProperty": {
                "x-tablename": "table 1",
                "type": "object",
                "x-mixins": "module.Mixin1",
                "properties": {"property_1": {"type": "integer"}},
            }
        },
    )

    assert hasattr(model, "property_2")
    assert model.__abstract__ is False


class TestGetSchema:
    """Tests for _get_schema."""

    @staticmethod
    @pytest.mark.parametrize(
        "schemas, exception",
        [
            ({}, exceptions.SchemaNotFoundError),
            (
                {"Schema": {"type": "object", "properties": {"key": "value"}}},
                exceptions.MalformedSchemaError,
            ),
            (
                {
                    "Schema": {
                        "allOf": [
                            {"type": "object", "properties": {"key": "value"}},
                            {"$ref": "#/components/schemas/Parent"},
                        ]
                    },
                    "Parent": {"x-inherits": True},
                },
                exceptions.MalformedSchemaError,
            ),
            (
                {"Schema": {"x-tablename": "schema", "properties": {"key": "value"}}},
                exceptions.FeatureNotImplementedError,
            ),
            (
                {
                    "Schema": {
                        "type": "string",
                        "x-tablename": "schema",
                        "properties": {"key": "value"},
                    }
                },
                exceptions.FeatureNotImplementedError,
            ),
            (
                {"Schema": {"type": "object", "x-tablename": "schema"}},
                exceptions.MalformedSchemaError,
            ),
            (
                {
                    "Schema": {
                        "type": "object",
                        "x-tablename": "schema",
                        "properties": {},
                    }
                },
                exceptions.MalformedSchemaError,
            ),
        ],
        ids=[
            "schema doesn't exist",
            "x-tablename and x-inherits missing",
            "x-inherits on parent",
            "type missing",
            "type not object",
            "properties missing",
            "properties empty",
        ],
    )
    @pytest.mark.model
    def test_invalid(schemas, exception):
        """
        GIVEN invalid schema and expected exception
        WHEN _get_schema is called with the schema
        THEN the expected exception is raised.
        """
        name = "Schema"

        with pytest.raises(exception):
            model_factory._get_schema(name, schemas)

    @staticmethod
    @pytest.mark.model
    def test_valid():
        """
        GIVEN valid schema
        WHEN _get_schema is called with the schema
        THEN the schema is returned.
        """
        name = "Schema"
        schema = {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"key": "value"},
        }
        schemas = {
            "Schema": {"$ref": "#/components/schemas/RefSchema"},
            "RefSchema": schema,
        }

        returned_schema = model_factory._get_schema(name, schemas)

        assert returned_schema == schema

    @staticmethod
    @pytest.mark.parametrize("inherits", [True, "RefSchema"], ids=["bool", "string"])
    @pytest.mark.model
    def test_valid_inherits(inherits):
        """
        GIVEN valid schema that inherits
        WHEN _get_schema is called with the schema
        THEN the schema exclusing the parent is returned.
        """
        name = "Schema"
        schema = {
            "allOf": [
                {
                    "type": "object",
                    "x-inherits": inherits,
                    "properties": {"key": "value"},
                },
                {"$ref": "#/components/schemas/RefSchema"},
            ]
        }
        ref_schema = {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"parent_key": "parent value"},
        }
        schemas = {"Schema": schema, "RefSchema": ref_schema}

        returned_schema = model_factory._get_schema(name, schemas)

        assert returned_schema == {
            "type": "object",
            "x-inherits": "RefSchema",
            "properties": {"key": "value"},
        }


class TestGetKwargs:
    """Tests for _get_kwargs."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "in_schema",
        [
            {"x-kwargs": {1: "value 1"}},
            {"x-kwargs": {"__tablename__": "value 1"}},
            {"x-kwargs": {"__table_args__": "value 1"}},
            {"x-kwargs": {"key": "value 1"}},
            {"x-kwargs": {"__key": "value 1"}},
            {"x-kwargs": {"key__": "value 1"}},
        ],
        ids=[
            "invalid kwargs",
            "__tablename__",
            "__table_args__",
            "no underscores",
            "front underscores",
            "back underscores",
        ],
    )
    @pytest.mark.model
    def test_invalid(in_schema):
        """
        GIVEN invalid kwargs
        WHEN _get_kwargs is called with the schema
        THEN MalformedExtensionPropertyError is raised.
        """
        with pytest.raises(exceptions.MalformedExtensionPropertyError):
            model_factory._get_kwargs(schema=in_schema)

    @staticmethod
    @pytest.mark.model
    def test_valid_exists():
        """
        GIVEN schema with kwargs
        WHEN _get_kwargs is called with the schema
        THEN the kwargs are returned.
        """
        in_schema = {"x-kwargs": {"__key__": "value"}}

        kwargs = model_factory._get_kwargs(schema=in_schema)

        assert kwargs == {"__key__": "value"}

    @staticmethod
    @pytest.mark.model
    def test_valid_not_exists():
        """
        GIVEN schema without kwargs
        WHEN _get_kwargs is called with the schema
        THEN empty dictionary is returned.
        """
        kwargs = model_factory._get_kwargs(schema={})

        assert kwargs == {}


@pytest.mark.model
def test_kwargs():
    """
    GIVEN schemas with schema that has kwargs
    WHEN model_factory is called with the name of the schema
    THEN a model with the kwargs is returned.
    """
    model = model_factory.model_factory(
        name="SingleProperty",
        get_base=_mock_get_base,
        schemas={
            "SingleProperty": {
                "x-tablename": "table 1",
                "type": "object",
                "properties": {"property_1": {"type": "integer"}},
                "x-kwargs": {"__mapper_args__": {"passive_deletes": True}},
            }
        },
    )

    assert model.__mapper_args__ == {"passive_deletes": True}


class TestPrepareModelDict:
    """Tests for _prepare_model_dict."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, expected_dict",
        [
            ({"x-tablename": "schema"}, {"__tablename__": "schema"}),
            ({"x-inherits": "Parent"}, {}),
            (
                {"x-inherits": "Parent", "x-tablename": "schema"},
                {"__tablename__": "schema"},
            ),
        ],
        ids=["not inherits", "inherits same tablename", "inherits different tablename"],
    )
    @pytest.mark.model
    def test_(schema, expected_dict):
        """
        GIVEN schema and expected dictionary
        WHEN _prepare_model_dict is called with the schema
        THEN the expected dictionary is returned.
        """
        returned_dict = model_factory._prepare_model_dict(schema=schema)

        assert expected_dict == returned_dict
