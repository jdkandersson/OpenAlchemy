"""Tests for the get_secondary association helper."""

import pytest

from open_alchemy.schemas.helpers import association

SCHEMA_TESTS = [
    pytest.param(
        {"items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-secondary": "association"}},
        id="items $ref",
    ),
    pytest.param(
        {"items": {"allOf": [{"x-secondary": "association"}]}},
        {},
        id="items allOf",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/ItemsSchema"},
        {"ItemsSchema": {"items": {"x-secondary": "association"}}},
        id="$ref",
    ),
    pytest.param(
        {"allOf": [{"items": {"x-secondary": "association"}}]},
        {},
        id="allOf",
    ),
    pytest.param(
        {
            "items": {
                "allOf": [
                    {"x-secondary": "association"},
                    {"$ref": "#/components/schemas/RefSchema"},
                ]
            }
        },
        {"RefSchema": {"x-secondary": "ref_association"}},
        id="items allOf secondary local and ref local first",
    ),
    pytest.param(
        {
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "association"},
                ]
            }
        },
        {"RefSchema": {"x-secondary": "ref_association"}},
        id="items allOf secondary local and ref local last",
    ),
]


@pytest.mark.parametrize("schema, schemas", SCHEMA_TESTS)
@pytest.mark.schemas
@pytest.mark.helper
def test_schema(schema, schemas):
    """
    GIVEN property schema and schemas
    WHEN get_secondary is called with the property schema and schemas
    THEN the expected secondary is returned.
    """
    returned_secondary = association.get_secondary(
        schema=schema,
        schemas=schemas,
    )

    assert returned_secondary == "association"
