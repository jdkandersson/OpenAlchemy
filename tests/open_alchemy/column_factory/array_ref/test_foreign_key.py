"""Tests for foreign key."""
# pylint: disable=protected-access

from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy.column_factory import array_ref


@pytest.mark.column
def test_schemas_missing():
    """
    GIVEN referenced model is not in models and not in schemas
    WHEN set_ is called with the referenced model name
    THEN MalformedRelationshipError is raised.
    """
    fk_column = "column_1"
    model_schema = {"properties": {fk_column: {"type": "integer"}}}

    with pytest.raises(exceptions.MalformedRelationshipError):
        array_ref._foreign_key.set_(
            ref_model_name="RefSchema",
            logical_name="logical name 1",
            model_schema=model_schema,
            schemas={},
            fk_column=fk_column,
        )


@pytest.mark.parametrize(
    "schemas",
    [
        {"RefSchema": {"type": "object", "properties": {}}},
        {"RefSchema": {"allOf": [{"type": "object", "properties": {}}]}},
    ],
    ids=["plain", "allOf exists"],
)
@pytest.mark.column
def test_schemas(schemas):
    """
    GIVEN referenced model is not in models, model schema, schemas and foreign key
        column
    WHEN set_ is called with the model schema, schemas and foreign key
        column
    THEN the foreign key column is added to the referenced model using allOf.
    """
    ref_model_name = "RefSchema"
    fk_column = "column_1"
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {fk_column: {"type": "integer"}},
    }

    array_ref._foreign_key.set_(
        ref_model_name=ref_model_name,
        logical_name="logical name 1",
        model_schema=model_schema,
        schemas=schemas,
        fk_column=fk_column,
    )

    assert schemas == {
        ref_model_name: {
            "allOf": [
                {"type": "object", "properties": {}},
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_logical name 1_{fk_column}": {
                            "type": "integer",
                            "x-foreign-key": f"{tablename}.{fk_column}",
                            "x-dict-ignore": True,
                        }
                    },
                },
            ]
        }
    }


@pytest.mark.column
def test_models(mocked_facades_models: mock.MagicMock):
    """
    GIVEN mocked models, referenced model is in models, model schema, schemas and
        foreign key column
    WHEN set_ is called with the model schema, schemas and foreign key
        column
    THEN the foreign key is added to the model.
    """
    ref_model_name = "RefSchema"
    fk_column = "column_1"
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {fk_column: {"type": "integer"}},
    }
    schemas = {ref_model_name: {"type": "object", "properties": {}}}
    mock_ref_model = mock.MagicMock()
    mocked_facades_models.get_model.return_value = mock_ref_model

    array_ref._foreign_key.set_(
        ref_model_name=ref_model_name,
        logical_name="logical name 1",
        model_schema=model_schema,
        schemas=schemas,
        fk_column=fk_column,
    )

    added_fk_column = getattr(mock_ref_model, f"{tablename}_logical name 1_{fk_column}")
    assert isinstance(added_fk_column.type, facades.sqlalchemy.column.Integer)
    foreign_key = list(added_fk_column.foreign_keys)[0]
    assert f"{tablename}.{fk_column}" in str(foreign_key)
    mocked_facades_models.get_model.assert_called_once_with(name=ref_model_name)


@pytest.mark.column
def test_fk_def():
    """
    GIVEN schema with array referencing another schema which already has foreign key
        and schemas
    WHEN handle_array is called
    THEN foreign key is not added to the referenced schema.
    """
    ref_model_name = "RefSchema"
    fk_column = "id"
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {
                f"{tablename}_logical name 1_id": {
                    "type": "integer",
                    "x-foreign-key": "schema.id",
                }
            },
        }
    }

    array_ref._foreign_key.set_(
        ref_model_name=ref_model_name,
        logical_name="logical name 1",
        model_schema=model_schema,
        schemas=schemas,
        fk_column=fk_column,
    )

    assert schemas == {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {
                f"{tablename}_logical name 1_id": {
                    "type": "integer",
                    "x-foreign-key": "schema.id",
                }
            },
        }
    }
