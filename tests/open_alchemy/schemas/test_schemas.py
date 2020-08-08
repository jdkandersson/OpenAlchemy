"""Tests for schemas."""

import pytest

from open_alchemy import exceptions
from open_alchemy.schemas import process


@pytest.mark.schemas
def test_process_invalid():
    """
    GIVEN invalid schemas
    WHEN process is called with the schemas
    THEN MalformedSchemaError is raised.
    """
    schemas = {"Schema": {"x-tablename": "schema"}}

    with pytest.raises(exceptions.MalformedSchemaError):
        process(schemas=schemas)


@pytest.mark.schemas
def test_process():
    """
    GIVEN schemas with back references and foreign keys
    WHEN process is called with the schemas
    THEN the back references and foreign keys are added to the schemas.
    """
    schemas = {
        "Schema1": {
            "x-tablename": "schema1",
            "type": "object",
            "properties": {
                "prop_1": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema1"},
                        {"x-backref": "schema1"},
                    ]
                }
            },
        },
        "RefSchema1": {
            "x-tablename": "ref_schema_1",
            "x-foreign-key-column": "prop_1",
            "type": "object",
            "properties": {"prop_1": {"type": "integer"}},
        },
    }

    process(schemas=schemas)

    expected_schemas = {
        "Schema1": {
            "allOf": [
                {
                    "x-tablename": "schema1",
                    "type": "object",
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema1"},
                                {"x-backref": "schema1"},
                            ]
                        }
                    },
                },
                {
                    "type": "object",
                    "properties": {
                        "prop_1_prop_1": {
                            "type": "integer",
                            "x-dict-ignore": True,
                            "nullable": True,
                            "x-foreign-key": "ref_schema_1.prop_1",
                        }
                    },
                },
            ]
        },
        "RefSchema1": {
            "allOf": [
                {
                    "x-tablename": "ref_schema_1",
                    "x-foreign-key-column": "prop_1",
                    "type": "object",
                    "properties": {"prop_1": {"type": "integer"}},
                },
                {
                    "type": "object",
                    "x-backrefs": {
                        "schema1": {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema1"},
                        }
                    },
                },
            ]
        },
    }
    assert schemas == expected_schemas
