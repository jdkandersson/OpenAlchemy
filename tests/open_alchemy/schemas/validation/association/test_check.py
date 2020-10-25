"""Tests for check function in association validation."""

import pytest

from open_alchemy.schemas.validation import association

TESTS = [
    pytest.param({}, True, id="empty"),
    pytest.param({"Schema": {}}, True, id="single not association"),
    pytest.param(
        {
            "Schema": {
                "type": "object",
                "x-tablename": "schema",
                "properties": {
                    "schema_primary_key": {
                        "type": "integer",
                        "x-primary-key": True,
                    },
                    "schema_many_to_many": {
                        "type": "array",
                        "items": {
                            "allOf": [
                                {"x-secondary": "association"},
                                {"$ref": "#/components/schemas/RefSchema"},
                            ]
                        },
                    },
                },
            },
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "properties": {
                    "ref_schema_primary_key": {
                        "type": "string",
                        "x-primary-key": True,
                    }
                },
            },
            "AssociationSchema": {
                "type": "object",
                "x-tablename": "association",
                "properties": {
                    "schema_prop": {
                        "type": "boolean",
                        "x-primary-key": True,
                    }
                },
            },
        },
        False,
        id="single association invalid",
    ),
    pytest.param(
        {
            "Schema": {
                "type": "object",
                "x-tablename": "schema",
                "properties": {
                    "schema_primary_key": {
                        "type": "integer",
                        "x-primary-key": True,
                    },
                    "schema_many_to_many": {
                        "type": "array",
                        "items": {
                            "allOf": [
                                {"x-secondary": "association"},
                                {"$ref": "#/components/schemas/RefSchema"},
                            ]
                        },
                    },
                },
            },
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "properties": {
                    "ref_schema_primary_key": {
                        "type": "string",
                        "x-primary-key": True,
                    }
                },
            },
            "AssociationSchema": {
                "type": "object",
                "x-tablename": "association",
                "properties": {
                    "schema_prop": {
                        "type": "integer",
                        "x-primary-key": True,
                        "x-foreign-key": "schema.schema_primary_key",
                    }
                },
            },
        },
        True,
        id="single association valid",
    ),
]


@pytest.mark.parametrize("schemas, expected_valid", TESTS)
@pytest.mark.schemas
@pytest.mark.validate
def test_check(schemas, expected_valid):
    """
    GIVEN schemas and expected valid
    WHEN check is called with the schemas
    THEN the expected valid is returned.
    """
    returned_result = association.check(schemas=schemas)

    assert returned_result.valid == expected_valid
