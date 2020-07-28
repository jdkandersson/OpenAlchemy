"""Tests for schemas."""

import pytest

from open_alchemy.schemas import process


@pytest.mark.schemas
def test_process():
    """
    GIVEN schemas with back references
    WHEN process is called with the schemas
    THEN the backreferences are added to the schemas.
    """
    schemas = {
        "Schema1": {
            "x-tablename": "schema1",
            "properties": {
                "prop_1": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema1"},
                        {"x-backref": "schema1"},
                    ]
                }
            },
        },
        "RefSchema1": {"ref_key_1": "ref_value 1"},
    }

    process(schemas=schemas)

    assert schemas == {
        "Schema1": {
            "x-tablename": "schema1",
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
            "allOf": [
                {"ref_key_1": "ref_value 1"},
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
