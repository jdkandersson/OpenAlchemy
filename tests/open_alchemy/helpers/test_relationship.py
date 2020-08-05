"""Tests for relationship helpers."""

import pytest

from open_alchemy.helpers import relationship


@pytest.mark.parametrize(
    "schema, schemas, expected_type",
    [
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            relationship.Type.MANY_TO_ONE,
            id="many-to-one $ref",
        ),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            relationship.Type.MANY_TO_ONE,
            id="many-to-one allOf",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "x-uselist": True}},
            relationship.Type.MANY_TO_ONE,
            id="many-to-one $ref uselist true",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "x-uselist": False}},
            relationship.Type.ONE_TO_ONE,
            id="one-to-one $ref",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False},
                ]
            },
            {"RefSchema": {"type": "object"}},
            relationship.Type.ONE_TO_ONE,
            id="many-to-one allOf",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False},
                ]
            },
            {"RefSchema": {"type": "object", "x-uselist": True}},
            relationship.Type.ONE_TO_ONE,
            id="many-to-one allOf and $ref",
        ),
        pytest.param(
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "object"}},
            relationship.Type.ONE_TO_MANY,
            id="many-to-one $ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/Schema"},
            {
                "Schema": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                },
                "RefSchema": {"type": "object"},
            },
            relationship.Type.ONE_TO_MANY,
            id="$ref many-to-one $ref",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                ]
            },
            {"RefSchema": {"type": "object"}},
            relationship.Type.ONE_TO_MANY,
            id="allOf many-to-one $ref",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                ]
            },
            {"RefSchema": {"type": "object"}},
            relationship.Type.ONE_TO_MANY,
            id="many-to-one allOf",
        ),
        pytest.param(
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"type": "object", "x-secondary": "schema_ref_schema"}},
            relationship.Type.MANY_TO_MANY,
            id="many-to-many $ref",
        ),
        pytest.param(
            {
                "type": "array",
                "items": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-secondary": "schema_ref_schema"},
                    ]
                },
            },
            {"RefSchema": {"type": "object"}},
            relationship.Type.MANY_TO_MANY,
            id="many-to-many allOf",
        ),
    ],
)
@pytest.mark.helper
def test_calculate_type(schema, schemas, expected_type):
    """
    GIVEN schema, schemas and expected type
    WHEN calculate_type is called with the schema and schemas
    THEN the expected type is returned.
    """
    returned_type = relationship.calculate_type(schema=schema, schemas=schemas)

    assert returned_type == expected_type
