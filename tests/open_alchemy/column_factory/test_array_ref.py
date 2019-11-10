"""Tests for array references."""

from unittest import mock

import pytest
import sqlalchemy

from open_alchemy import exceptions
from open_alchemy.column_factory import array_ref


@pytest.mark.parametrize(
    "spec, schemas",
    [
        ({"type": "array"}, {}),
        ({"type": "array", "items": {}}, {}),
        ({"type": "array", "items": {"allOf": []}}, {}),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "ref 1"}, {"$ref": "ref 2"}]},
            },
            {},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
        ),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            },
            {"RefSchema": {}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "integer"}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "object"}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "x-backref": "schema",
                    "x-uselist": False,
                }
            },
        ),
    ],
    ids=[
        "no items",
        "items without $ref and allOf",
        "items allOf without $ref",
        "items allOf multiple $ref",
        "$ref items no type",
        "allOf items no type",
        "items type not object",
        "items no x-tablename",
        "backref and uselist defined",
    ],
)
@pytest.mark.column
def test_handle_array_invalid(spec, schemas):
    """
    GIVEN array schema that is not valid and schemas
    WHEN handle_array is called
    THEN MalformedRelationshipError is raised.
    """
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }

    with pytest.raises(exceptions.MalformedRelationshipError):
        array_ref.handle_array(
            spec=spec,
            model_schema=model_schema,
            schemas=schemas,
            logical_name="ref_schema",
        )


@pytest.mark.parametrize(
    "spec, schemas",
    [
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        ),
        (
            {"$ref": "#/components/schemas/Schema"},
            {
                "Schema": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                },
                "RefSchema": {"type": "object", "x-tablename": "ref_schema"},
            },
        ),
        (
            {
                "allOf": [
                    {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                ]
            },
            {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        ),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            },
            {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"allOf": [{"type": "object", "x-tablename": "ref_schema"}]}},
        ),
    ],
    ids=[
        "array items $ref",
        "$ref array items $ref",
        "allOf array items $ref",
        "array items allOf $ref",
        "array items $ref allOf",
    ],
)
@pytest.mark.column
def test_handle_array_relationship(spec, schemas):
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN handle_array is called
    THEN relationship is returned pointing to the referenced schema.
    """
    logical_name = "ref_schema"
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }

    ([(tbl_logical_name, relationship)], schema_spec) = array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name=logical_name
    )

    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert tbl_logical_name == logical_name
    assert schema_spec == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }


@pytest.mark.column
def test_handle_array_relationship_backref():
    """
    GIVEN schema with array referencing another schema with backref and schemas
    WHEN handle_array is called
    THEN relationship with backref is returned.
    """
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "x-backref": "schema",
        }
    }
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {"id": {"type": "integer"}},
    }

    ([(_, relationship)], _) = array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert relationship.backref == "schema"


@pytest.mark.column
def test_handle_array_schemas():
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN handle_array is called
    THEN foreign key is added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}}

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "allOf": [
                {"type": "object", "x-tablename": "ref_schema"},
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_id": {
                            "type": "integer",
                            "x-foreign-key": f"{tablename}.id",
                            "x-dict-ignore": True,
                        }
                    },
                },
            ]
        }
    }


@pytest.mark.column
def test_handle_array_schemas_foreign_key_column():
    """
    GIVEN schema with array referencing another schema with foreign key and schemas
    WHEN handle_array is called
    THEN foreign key is added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"fk_column": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "x-foreign-key-column": "fk_column",
        }
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "allOf": [
                {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "x-foreign-key-column": "fk_column",
                },
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_fk_column": {
                            "type": "integer",
                            "x-foreign-key": f"{tablename}.fk_column",
                            "x-dict-ignore": True,
                        }
                    },
                },
            ]
        }
    }


@pytest.mark.column
def test_set_foreign_key_schemas_missing():
    """
    GIVEN referenced model is not in models and not in schemas
    WHEN _set_foreign_key is called with the referenced model name
    THEN MalformedRelationshipError is raised.
    """
    fk_column = "column_1"
    model_schema = {
        "type": "object",
        "x-tablename": "schema",
        "properties": {fk_column: {"type": "integer"}},
    }

    with pytest.raises(exceptions.MalformedRelationshipError):
        array_ref._set_foreign_key(  # pylint: disable=protected-access
            ref_model_name="RefSchema",
            model_schema=model_schema,
            schemas={},
            fk_column=fk_column,
        )


@pytest.mark.column
def test_set_foreign_key_schemas():
    """
    GIVEN referenced model is not in models, model schema, schemas and foreign key
        column
    WHEN _set_foreign_key is called with the model schema, schemas and foreign key
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
    schemas = {ref_model_name: {"type": "object"}}

    array_ref._set_foreign_key(  # pylint: disable=protected-access
        ref_model_name=ref_model_name,
        model_schema=model_schema,
        schemas=schemas,
        fk_column=fk_column,
    )

    assert schemas == {
        ref_model_name: {
            "allOf": [
                {"type": "object"},
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_{fk_column}": {
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
def test_set_foreign_key_models(mocked_models: mock.MagicMock):
    """
    GIVEN mocked models, referenced model is in models, model schema, schemas and
        foreign key column
    WHEN _set_foreign_key is called with the model schema, schemas and foreign key
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
    schemas = {ref_model_name: {"type": "object"}}
    mock_ref_model = mock.MagicMock()
    setattr(mocked_models, ref_model_name, mock_ref_model)

    array_ref._set_foreign_key(  # pylint: disable=protected-access
        ref_model_name=ref_model_name,
        model_schema=model_schema,
        schemas=schemas,
        fk_column=fk_column,
    )

    added_fk_column = getattr(mock_ref_model, f"{tablename}_{fk_column}")
    assert isinstance(added_fk_column.type, sqlalchemy.Integer)
    foreign_key = list(added_fk_column.foreign_keys)[0]
    assert f"{tablename}.{fk_column}" in str(foreign_key)
