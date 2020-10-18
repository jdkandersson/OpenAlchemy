"""Tests for property_ helpers."""

import pytest

from open_alchemy.helpers import property_

CALCULATE_TYPE_TESTS = [
    pytest.param(
        {"x-json": True},
        {},
        property_.Type.JSON,
        id="x-json True",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-json": True}},
        property_.Type.JSON,
        id="x-json True $ref",
    ),
    pytest.param(
        {"allOf": [{"x-json": True}]},
        {},
        property_.Type.JSON,
        id="x-json True allOf",
    ),
    pytest.param(
        {"x-json": False, "type": "object"},
        {},
        property_.Type.RELATIONSHIP,
        id="object x-json false",
    ),
    pytest.param(
        {"x-json": False, "type": "integer"},
        {},
        property_.Type.SIMPLE,
        id="integer x-json false",
    ),
    pytest.param(
        {"readOnly": True, "type": "integer"},
        {},
        property_.Type.SIMPLE,
        id="readOnly True integer",
    ),
    pytest.param(
        {"readOnly": True, "type": "number"},
        {},
        property_.Type.SIMPLE,
        id="readOnly True number",
    ),
    pytest.param(
        {"readOnly": True, "type": "string"},
        {},
        property_.Type.SIMPLE,
        id="readOnly True string",
    ),
    pytest.param(
        {"readOnly": True, "type": "boolean"},
        {},
        property_.Type.SIMPLE,
        id="readOnly True boolean",
    ),
    pytest.param(
        {"readOnly": True, "type": "object"},
        {},
        property_.Type.BACKREF,
        id="readOnly True object",
    ),
    pytest.param(
        {"readOnly": True, "type": "array"},
        {},
        property_.Type.BACKREF,
        id="readOnly True array",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"readOnly": True, "type": "object"}},
        property_.Type.BACKREF,
        id="readOnly True $ref",
    ),
    pytest.param(
        {"allOf": [{"readOnly": True, "type": "object"}]},
        {},
        property_.Type.BACKREF,
        id="readOnly True allOf",
    ),
    pytest.param(
        {"readOnly": False, "type": "object"},
        {},
        property_.Type.RELATIONSHIP,
        id="object readOnly false",
    ),
    pytest.param(
        {"readOnly": False, "type": "integer"},
        {},
        property_.Type.SIMPLE,
        id="integer readOnly false",
    ),
    pytest.param(
        {"readOnly": True, "x-json": True, "type": "object"},
        {},
        property_.Type.JSON,
        id="object readOnly and x-json True",
    ),
    pytest.param(
        {"type": "object"},
        {},
        property_.Type.RELATIONSHIP,
        id="object",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        property_.Type.RELATIONSHIP,
        id="object $ref",
    ),
    pytest.param(
        {"allOf": [{"type": "object"}]},
        {},
        property_.Type.RELATIONSHIP,
        id="object allOf",
    ),
    pytest.param(
        {"type": "array"},
        {},
        property_.Type.RELATIONSHIP,
        id="array",
    ),
    pytest.param(
        {"type": "integer"},
        {},
        property_.Type.SIMPLE,
        id="simple",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_type", CALCULATE_TYPE_TESTS)
@pytest.mark.helper
def test_calculate_type(schema, schemas, expected_type):
    """
    GIVEN schema, schemas and expected type
    WHEN calculate_type is called with the schema and schemas
    THEN the expected type is returned.
    """
    returned_type = property_.calculate_type(schema=schema, schemas=schemas)

    assert returned_type == expected_type
