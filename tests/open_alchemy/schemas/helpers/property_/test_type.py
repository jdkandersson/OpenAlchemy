"""Tests for type helpers."""

import pytest

from open_alchemy.schemas.helpers.property_ import type_

CALCULATE_TYPE_TESTS = [
    pytest.param(
        {"x-json": True},
        {},
        type_.Type.JSON,
        id="x-json True",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-json": True}},
        type_.Type.JSON,
        id="x-json True $ref",
    ),
    pytest.param(
        {"allOf": [{"x-json": True}]},
        {},
        type_.Type.JSON,
        id="x-json True allOf",
    ),
    pytest.param(
        {"x-json": False, "type": "object"},
        {},
        type_.Type.RELATIONSHIP,
        id="object x-json false",
    ),
    pytest.param(
        {"x-json": False, "type": "integer"},
        {},
        type_.Type.SIMPLE,
        id="integer x-json false",
    ),
    pytest.param(
        {"readOnly": True, "type": "integer"},
        {},
        type_.Type.SIMPLE,
        id="readOnly True integer",
    ),
    pytest.param(
        {"readOnly": True, "type": "number"},
        {},
        type_.Type.SIMPLE,
        id="readOnly True number",
    ),
    pytest.param(
        {"readOnly": True, "type": "string"},
        {},
        type_.Type.SIMPLE,
        id="readOnly True string",
    ),
    pytest.param(
        {"readOnly": True, "type": "boolean"},
        {},
        type_.Type.SIMPLE,
        id="readOnly True boolean",
    ),
    pytest.param(
        {"readOnly": True, "type": "object"},
        {},
        type_.Type.BACKREF,
        id="readOnly True object",
    ),
    pytest.param(
        {"readOnly": True, "type": "array"},
        {},
        type_.Type.BACKREF,
        id="readOnly True array",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"readOnly": True, "type": "object"}},
        type_.Type.BACKREF,
        id="readOnly True $ref",
    ),
    pytest.param(
        {"allOf": [{"readOnly": True, "type": "object"}]},
        {},
        type_.Type.BACKREF,
        id="readOnly True allOf",
    ),
    pytest.param(
        {"readOnly": False, "type": "object"},
        {},
        type_.Type.RELATIONSHIP,
        id="object readOnly false",
    ),
    pytest.param(
        {"readOnly": False, "type": "integer"},
        {},
        type_.Type.SIMPLE,
        id="integer readOnly false",
    ),
    pytest.param(
        {"readOnly": True, "x-json": True, "type": "object"},
        {},
        type_.Type.JSON,
        id="object readOnly and x-json True",
    ),
    pytest.param(
        {"type": "object"},
        {},
        type_.Type.RELATIONSHIP,
        id="object",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        type_.Type.RELATIONSHIP,
        id="object $ref",
    ),
    pytest.param(
        {"allOf": [{"type": "object"}]},
        {},
        type_.Type.RELATIONSHIP,
        id="object allOf",
    ),
    pytest.param(
        {"type": "array"},
        {},
        type_.Type.RELATIONSHIP,
        id="array",
    ),
    pytest.param(
        {"type": "integer"},
        {},
        type_.Type.SIMPLE,
        id="simple",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_type", CALCULATE_TYPE_TESTS)
@pytest.mark.schemas
def test_calculate_type(schema, schemas, expected_type):
    """
    GIVEN schema, schemas and expected type
    WHEN calculate_type is called with the schema and schemas
    THEN the expected type is returned.
    """
    returned_type = type_.calculate(schema=schema, schemas=schemas)

    assert returned_type == expected_type
