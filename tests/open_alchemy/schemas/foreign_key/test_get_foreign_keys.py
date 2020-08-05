"""Tests for foreign key pre-processor."""

import pytest

# from open_alchemy.schemas import foreign_key

GET_FOREIGN_KEYS_TESTS = [
    pytest.param({"Schema1": {}}, [], id="single schema not constructable",),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        [],
        id="single schema no foreign key",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}
                },
            },
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
        },
        [
            (
                "Schema1",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="single schema foreign key",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {"prop_2": {"type": "string"}},
            },
        },
        [],
        id="multiple schemas no foreign key",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}
                },
            },
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {"prop_2": {"type": "string"}},
            },
        },
        [
            (
                "Schema1",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple schemas first foreign key",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"}
                },
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
                "Schema2",
                "ref_schema_2_prop_2",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_2.prop_2",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple schemas second foreign key",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}
                },
            },
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"}
                },
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
                "Schema1",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
            (
                "Schema2",
                "ref_schema_2_prop_2",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_2.prop_2",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple schemas all foreign key",
    ),
]


# class TestGetForeignKeys:
#     """Tests for _get_foreign_keys"""

#     # pylint: disable=protected-access

#     @staticmethod
#     @pytest.mark.parametrize("schemas, expected_foreign_keys", GET_FOREIGN_KEYS_TESTS)
#     @pytest.mark.schemas
#     def test_(schemas, expected_foreign_keys):
#         """
#         GIVEN schemas and expected foreign keys
#         WHEN _get_foreign keys is called with the schemas
#         THEN the expected foreign keys are returned.
#         """
#         returned_foreign_keys = foreign_key._get_foreign_keys(schemas=schemas)

#         assert list(returned_foreign_keys) == expected_foreign_keys
