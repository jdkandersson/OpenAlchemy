"""Tests for array references."""

import sys

import pytest

from open_alchemy.column_factory import array_ref


@pytest.mark.parametrize(
    "spec, schemas",
    [
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {"$ref": "#/components/schemas/Schema"},
            {
                "Schema": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                },
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                },
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
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {
                "type": "array",
                "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            },
            {
                "RefSchema": {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {},
                }
            },
        ),
        (
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "allOf": [
                        {
                            "type": "object",
                            "x-tablename": "ref_schema",
                            "properties": {},
                        }
                    ]
                }
            },
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
    assert relationship.secondary is None
    assert tbl_logical_name == logical_name
    assert schema_spec == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }


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
    schemas = {
        "RefSchema": {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "allOf": [
                {"type": "object", "x-tablename": "ref_schema", "properties": {}},
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
def test_handle_array_schemas_fk_def():
    """
    GIVEN schema with array referencing another schema which already has foreign key
        and schemas
    WHEN handle_array is called
    THEN foreign key is not added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {
                "schema_id": {"type": "integer", "x-foreign-key": "schema.id"}
            },
        }
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert schemas == {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {
                "schema_id": {"type": "integer", "x-foreign-key": "schema.id"}
            },
        }
    }


@pytest.mark.column
def test_handle_array_schemas_fk_def_all_of():
    """
    GIVEN schema with array referencing another schema which has allOf which already
        has foreign key and schemas
    WHEN handle_array is called
    THEN foreign key is not added to the referenced schema.
    """
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    spec = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {
            "allOf": [
                {
                    "type": "object",
                    "x-tablename": "ref_schema",
                    "properties": {
                        "schema_id": {"type": "integer", "x-foreign-key": "schema.id"}
                    },
                }
            ]
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
                    "properties": {
                        "schema_id": {"type": "integer", "x-foreign-key": "schema.id"}
                    },
                }
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
            "properties": {},
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
                    "properties": {},
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
def test_handle_array_secondary(mocked_facades_models):
    """
    GIVEN schema with array referencing another schema and secondary set and schemas
    WHEN handle_array is called
    THEN table is set on models.
    """
    secondary = "association"
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer", "x-primary-key": True}},
    }
    spec = {
        "type": "array",
        "items": {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-secondary": secondary},
            ]
        },
    }
    schemas = {
        "RefSchema": {
            "type": "object",
            "x-tablename": "ref_schema",
            "properties": {"id": {"type": "integer", "x-primary-key": True}},
        }
    }

    array_ref.handle_array(
        spec=spec, model_schema=model_schema, schemas=schemas, logical_name="ref_schema"
    )

    assert mocked_facades_models.set_association.call_count == 1
    if sys.version_info[1] == 8:
        name = mocked_facades_models.set_association.call_args.kwargs["name"]
        table = mocked_facades_models.set_association.call_args.kwargs["table"]
    else:
        _, kwargs = mocked_facades_models.set_association.call_args
        name = kwargs["name"]
        table = kwargs["table"]
    assert name == secondary
    assert table.name == secondary
