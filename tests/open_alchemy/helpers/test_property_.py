"""Tests for property_ helpers."""

import pytest

from open_alchemy import types
from open_alchemy.helpers import property_

CALCULATE_TYPE_TESTS = [
    pytest.param(
        {"x-json": True},
        {},
        types.PropertyType.JSON,
        id="x-json True",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-json": True}},
        types.PropertyType.JSON,
        id="x-json True $ref",
    ),
    pytest.param(
        {"allOf": [{"x-json": True}]},
        {},
        types.PropertyType.JSON,
        id="x-json True allOf",
    ),
    pytest.param(
        {"x-json": False, "type": "object"},
        {},
        types.PropertyType.RELATIONSHIP,
        id="object x-json false",
    ),
    pytest.param(
        {"x-json": False, "type": "integer"},
        {},
        types.PropertyType.SIMPLE,
        id="integer x-json false",
    ),
    pytest.param(
        {"readOnly": True, "type": "integer"},
        {},
        types.PropertyType.SIMPLE,
        id="readOnly True integer",
    ),
    pytest.param(
        {"readOnly": True, "type": "number"},
        {},
        types.PropertyType.SIMPLE,
        id="readOnly True number",
    ),
    pytest.param(
        {"readOnly": True, "type": "string"},
        {},
        types.PropertyType.SIMPLE,
        id="readOnly True string",
    ),
    pytest.param(
        {"readOnly": True, "type": "boolean"},
        {},
        types.PropertyType.SIMPLE,
        id="readOnly True boolean",
    ),
    pytest.param(
        {"readOnly": True, "type": "object"},
        {},
        types.PropertyType.BACKREF,
        id="readOnly True object",
    ),
    pytest.param(
        {"readOnly": True, "type": "array"},
        {},
        types.PropertyType.BACKREF,
        id="readOnly True array",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"readOnly": True, "type": "object"}},
        types.PropertyType.BACKREF,
        id="readOnly True $ref",
    ),
    pytest.param(
        {"allOf": [{"readOnly": True, "type": "object"}]},
        {},
        types.PropertyType.BACKREF,
        id="readOnly True allOf",
    ),
    pytest.param(
        {"readOnly": False, "type": "object"},
        {},
        types.PropertyType.RELATIONSHIP,
        id="object readOnly false",
    ),
    pytest.param(
        {"readOnly": False, "type": "integer"},
        {},
        types.PropertyType.SIMPLE,
        id="integer readOnly false",
    ),
    pytest.param(
        {"readOnly": True, "x-json": True, "type": "object"},
        {},
        types.PropertyType.JSON,
        id="object readOnly and x-json True",
    ),
    pytest.param(
        {"type": "object"},
        {},
        types.PropertyType.RELATIONSHIP,
        id="object",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        types.PropertyType.RELATIONSHIP,
        id="object $ref",
    ),
    pytest.param(
        {"allOf": [{"type": "object"}]},
        {},
        types.PropertyType.RELATIONSHIP,
        id="object allOf",
    ),
    pytest.param(
        {"type": "array"},
        {},
        types.PropertyType.RELATIONSHIP,
        id="array",
    ),
    pytest.param(
        {"type": "integer"},
        {},
        types.PropertyType.SIMPLE,
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
