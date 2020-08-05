"""Tests for foreign key pre-processor."""

import pytest

from open_alchemy.schemas import foreign_key

GET_SCHEMA_FOREIGN_KEYS_TESTS = [
    pytest.param(
        "Schema",
        {"properties": {"prop_1": {"type": "integer"}}},
        {},
        [],
        id="single property no foreign key",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema1"},
                }
            }
        },
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-secondary": "schema_ref_schema",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        [],
        id="single property many-to-many",
    ),
    pytest.param(
        "Schema",
        {"properties": {"ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}}},
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        [
            (
                "Schema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="single property foreign key",
    ),
    pytest.param(
        "OtherSchema",
        {"properties": {"ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}}},
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        [
            (
                "OtherSchema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="single property foreign key different name",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
            }
        },
        {"RefSchema1": {"type": "integer"}, "RefSchema2": {"type": "integer"}},
        [],
        id="multiple property no foreign key",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
            }
        },
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "RefSchema2": {"type": "integer"},
        },
        [
            (
                "Schema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple property first foreign key",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
            }
        },
        {
            "RefSchema1": {"type": "integer"},
            "RefSchema2": {
                "x-tablename": "ref_schema_2",
                "x-foreign-key-column": "prop_2",
                "type": "object",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        [
            (
                "Schema",
                "ref_schema_2_prop_2",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_2.prop_2",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple property second foreign key",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
            }
        },
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "RefSchema2": {
                "x-tablename": "ref_schema_2",
                "x-foreign-key-column": "prop_2",
                "type": "object",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        [
            (
                "Schema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
            (
                "Schema",
                "ref_schema_2_prop_2",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_2.prop_2",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple property all foreign keys",
    ),
    pytest.param(
        "Schema",
        {
            "allOf": [
                {"$ref": "#/components/schemas/ParentSchema"},
                {
                    "x-inherits": True,
                    "properties": {
                        "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                    },
                },
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
                },
            },
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "RefSchema2": {
                "x-tablename": "ref_schema_2",
                "x-foreign-key-column": "prop_2",
                "type": "object",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        [
            (
                "Schema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            )
        ],
        id="multiple property first foreign key inheritance",
    ),
]


class TestGetSchemaForeignKeys:
    """Tests for _get_schema_foreign_keys"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema_name, schema, schemas, expected_foreign_keys",
        GET_SCHEMA_FOREIGN_KEYS_TESTS,
    )
    @pytest.mark.schemas
    def test_(schema_name, schema, schemas, expected_foreign_keys):
        """
        GIVEN schema name and schema, schemas and expected foreign keys
        WHEN _get_schema_foreign_keys is called with the schema name, schema and schemas
        THEN the expected foreign keys are returned.
        """
        returned_foreign_keys = foreign_key._get_schema_foreign_keys(
            schemas, schema_name, schema
        )

        assert list(returned_foreign_keys) == expected_foreign_keys
