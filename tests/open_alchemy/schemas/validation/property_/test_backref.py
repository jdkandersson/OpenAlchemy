"""Tests for readOnly property validator pre-processor."""

import pytest

from open_alchemy.schemas.validation.property_ import backref

TESTS = [
    pytest.param(
        {"type": "not supported"},
        {},
        (False, "not supported type is not supported"),
        id="type simple not supported",
    ),
    pytest.param(
        {"type": "object"},
        {},
        (True, None),
        id="type object no properties",
    ),
    pytest.param(
        {"type": "object", "properties": True},
        {},
        (False, "value of properties must be a dictionary"),
        id="type object properties not dict",
    ),
    pytest.param(
        {"type": "object", "properties": {True: {}}},
        {},
        (False, "property names must be strings, True is not"),
        id="type object properties keys not string",
    ),
    pytest.param(
        {"type": "object", "properties": {"prop_1": {}}},
        {},
        (False, "malformed schema :: Every property requires a type. "),
        id="type object properties property no type",
    ),
    pytest.param(
        {"type": "object", "properties": {"prop_1": {"type": "not simple"}}},
        {},
        (
            False,
            "properties :: prop_1 :: readOnly object propeerties do not support the "
            "not simple type",
        ),
        id="type object properties property not simple type",
    ),
    pytest.param(
        {
            "type": "object",
            "properties": {"prop_1": {"$ref": "#/components/schemas/RefSchema"}},
        },
        {},
        (False, "reference :: 'RefSchema was not found in schemas.' "),
        id="type object properties $ref unresolved",
    ),
    pytest.param(
        {
            "type": "object",
            "properties": {"prop_1": {"$ref": "#/components/schemas/RefSchema"}},
        },
        {"RefSchema": {"type": "not simple"}},
        (
            False,
            "properties :: prop_1 :: readOnly object propeerties do not support the "
            "not simple type",
        ),
        id="type object properties $ref property not simple type",
    ),
    pytest.param(
        {
            "type": "object",
            "properties": {"prop_1": {"allOf": [{"type": "not simple"}]}},
        },
        {},
        (
            False,
            "properties :: prop_1 :: readOnly object propeerties do not support the "
            "not simple type",
        ),
        id="type object properties property allOf not simple type",
    ),
    pytest.param(
        {
            "allOf": [
                {"type": "object", "properties": {"prop_1": {"type": "not simple"}}},
                {"type": "object", "properties": {"prop_2": {"type": "integer"}}},
            ]
        },
        {},
        (
            False,
            "properties :: prop_1 :: readOnly object propeerties do not support the "
            "not simple type",
        ),
        id="type object allOf first properties property not simple type",
    ),
    pytest.param(
        {
            "allOf": [
                {"type": "object", "properties": {"prop_1": {"type": "integer"}}},
                {"type": "object", "properties": {"prop_2": {"type": "not simple"}}},
            ]
        },
        {},
        (
            False,
            "properties :: prop_2 :: readOnly object propeerties do not support the "
            "not simple type",
        ),
        id="type object allOf second properties property not simple type",
    ),
    pytest.param(
        {"type": "object", "properties": {"prop_1": {"type": "integer"}}},
        {},
        (True, None),
        id="type object properties integer property",
    ),
    pytest.param(
        {"type": "object", "properties": {"prop_1": {"type": "number"}}},
        {},
        (True, None),
        id="type object properties number property",
    ),
    pytest.param(
        {"type": "object", "properties": {"prop_1": {"type": "string"}}},
        {},
        (True, None),
        id="type object properties string property",
    ),
    pytest.param(
        {"type": "object", "properties": {"prop_1": {"type": "boolean"}}},
        {},
        (True, None),
        id="type object properties boolean property",
    ),
    pytest.param(
        {
            "description": True,
            "type": "object",
            "properties": {"prop_1": {"type": "integer"}},
        },
        {},
        (False, "malformed schema :: A description value must be of type string. "),
        id="description not string",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "description": True,
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        (False, "malformed schema :: A description value must be of type string. "),
        id="$ref description not string",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "description": True,
                    "type": "object",
                    "properties": {"prop_1": {"type": "integer"}},
                }
            ]
        },
        {},
        (False, "malformed schema :: A description value must be of type string. "),
        id="allOf description not string",
    ),
    pytest.param(
        {
            "description": "description 1",
            "type": "object",
            "properties": {"prop_1": {"type": "integer"}},
        },
        {},
        (True, None),
        id="description valid",
    ),
    pytest.param(
        {"type": "array"},
        {},
        (False, "readOnly array properties must define items"),
        id="type array no items",
    ),
    pytest.param(
        {"type": "array", "items": True},
        {},
        (False, "malformed schema :: The items property must be of type dict. "),
        id="type array items not list",
    ),
    pytest.param(
        {"type": "array", "items": {}},
        {},
        (False, "malformed schema :: Every property requires a type. "),
        id="type array items type missing",
    ),
    pytest.param(
        {"type": "array", "items": {"type": "not object"}},
        {},
        (False, "items :: readOnly array items must have the object type"),
        id="type array items not object",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "not object"}},
        (False, "items :: readOnly array items must have the object type"),
        id="type array $ref items not object",
    ),
    pytest.param(
        {"type": "array", "items": {"allOf": [{"type": "not object"}]}},
        {},
        (False, "items :: readOnly array items must have the object type"),
        id="type array items allOf not object",
    ),
    pytest.param(
        {"type": "array", "items": {"type": "object"}},
        {},
        (True, None),
        id="type array object no properties",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {"type": "object", "properties": {"prop_1": {"type": "object"}}},
        },
        {},
        (
            False,
            "items :: properties :: prop_1 :: readOnly object propeerties do not "
            "support the object type",
        ),
        id="type array object property not simple",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_result", TESTS)
@pytest.mark.schemas
@pytest.mark.validation
def test_check(schema, schemas, expected_result):
    """
    GIVEN schemas, schema and the expected result
    WHEN check is called with the schemas schema
    THEN the expected result is returned.
    """
    returned_result = backref.check(schemas, schema)

    assert returned_result == expected_result
