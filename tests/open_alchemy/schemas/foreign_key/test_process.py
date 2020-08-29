"""Tests for foreign key schemas processing."""

import pytest

from open_alchemy.schemas import foreign_key

PROCESS_TESTS = [
    pytest.param(
        {},
        {},
        id="empty",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        id="single no foreign key",
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
        {
            "Schema1": {
                "allOf": [
                    {
                        "x-tablename": "schema_1",
                        "properties": {
                            "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}
                        },
                    },
                    {
                        "type": "object",
                        "properties": {
                            "ref_schema_1_prop_1": {
                                "type": "integer",
                                "x-foreign-key": "ref_schema_1.prop_1",
                                "x-dict-ignore": True,
                                "nullable": True,
                            }
                        },
                    },
                ]
            },
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
        },
        id="single foreign key",
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
        {
            "Schema1": {
                "allOf": [
                    {
                        "x-tablename": "schema_1",
                        "properties": {
                            "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}
                        },
                    },
                    {
                        "type": "object",
                        "properties": {
                            "ref_schema_1_prop_1": {
                                "type": "integer",
                                "x-foreign-key": "ref_schema_1.prop_1",
                                "x-dict-ignore": True,
                                "nullable": True,
                            }
                        },
                    },
                ]
            },
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "allOf": [
                    {
                        "x-tablename": "schema_2",
                        "properties": {
                            "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"}
                        },
                    },
                    {
                        "type": "object",
                        "properties": {
                            "ref_schema_2_prop_2": {
                                "type": "integer",
                                "x-foreign-key": "ref_schema_2.prop_2",
                                "x-dict-ignore": True,
                                "nullable": True,
                            }
                        },
                    },
                ]
            },
            "RefSchema2": {
                "x-tablename": "ref_schema_2",
                "x-foreign-key-column": "prop_2",
                "type": "object",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        id="multiple foreign keys",
    ),
]


@pytest.mark.parametrize("schemas, expected_schemas", PROCESS_TESTS)
@pytest.mark.schemas
def test_process(schemas, expected_schemas):
    """
    GIVEN schemas and expected schemas
    WHEN process is called with the schemas
    THEN the expected schemas are modified so that they are equal to the expected
        schemas.
    """
    foreign_key.process(schemas=schemas)

    assert schemas == expected_schemas
