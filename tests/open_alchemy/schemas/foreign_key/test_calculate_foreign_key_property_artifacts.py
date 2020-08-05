"""Tests for foreign key pre-processor."""

import pytest

from open_alchemy.schemas import foreign_key

CALC_F_K_PROP_ART_TESTS = [
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
                "nullable": False,
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": False,
            },
        ),
        id="many-to-one not nullable",
    ),
    pytest.param(
        "Schema",
        {"required": []},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one not required",
    ),
    pytest.param(
        "Schema",
        {"required": ["ref_schema"]},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": False,
            },
        ),
        id="many-to-one required",
    ),
    pytest.param(
        "Schema",
        {
            "x-tablename": "schema",
            "required": ["ref_schema"],
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schema",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-tablename": "ref_schema"}},
        (
            "RefSchema",
            "schema_ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="one-to-many required",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "format": "int32"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "format": "int32",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one format",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "string", "maxLength": 1}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "string",
                "maxLength": 1,
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one maxLength",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "default": 1}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "default": 1,
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": False,
            },
        ),
        id="many-to-one default",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-primary-key",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-autoincrement": True}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-autoincrement",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-index": True}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-index",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-unique": True}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-unique",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-foreign-key": "other.key"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-foreign-key",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-kwargs": {}}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-kwargs",
    ),
    pytest.param(
        "Schema",
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schema",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-tablename": "ref_schema"}},
        (
            "RefSchema",
            "schema_ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="one-to-many",
    ),
    pytest.param(
        "Schema",
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schema",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-tablename": "ref_schema", "nullable": False}},
        (
            "RefSchema",
            "schema_ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="one-to-many reference not nullable",
    ),
    pytest.param(
        "Schema",
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schema",
        {
            "type": "array",
            "nullable": False,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"x-tablename": "ref_schema"}},
        (
            "RefSchema",
            "schema_ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="one-to-many property not nullable",
    ),
]


class TestCalculateForeignKeyPropertyArtifacts:
    """Tests for _calculate_foreign_key_property_artifacts"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "parent_name, parent_schema, property_name, property_schema, schemas, "
        "expected_schema",
        CALC_F_K_PROP_ART_TESTS,
    )
    @pytest.mark.schemas
    def test_(
        parent_name,
        parent_schema,
        property_name,
        property_schema,
        schemas,
        expected_schema,
    ):
        """
        GIVEN schemas, parent schema, property name and schema and expected schema
        WHEN _calculate_foreign_key_property_artifacts is called with the schemas,
            parent schema and property name and schema
        THEN the expected schema is returned.
        """
        returned_schema = foreign_key._calculate_foreign_key_property_artifacts(
            schemas, parent_name, parent_schema, property_name, property_schema
        )

        assert returned_schema == expected_schema
