"""Tests for the property validation."""

import pytest

from open_alchemy.schemas.validation import property_

CHECK_TYPE_TESTS = [
    pytest.param(
        True,
        {},
        (False, "malformed schema :: The schema must be a dictionary. "),
        id="not dictionary",
    ),
    pytest.param(
        {},
        {},
        (False, "malformed schema :: Every property requires a type. "),
        id="type not valid",
    ),
    pytest.param(
        {"type": "not supported"},
        {},
        (False, "not supported is not a supported type"),
        id="type not supported",
    ),
    pytest.param({"type": "integer"}, {}, (True, None), id="type integer"),
    pytest.param({"type": "number"}, {}, (True, None), id="type number"),
    pytest.param({"type": "string"}, {}, (True, None), id="type string"),
    pytest.param({"type": "boolean"}, {}, (True, None), id="type boolean"),
    pytest.param({"type": "object"}, {}, (True, None), id="type object"),
    pytest.param({"type": "array"}, {}, (True, None), id="type array"),
    pytest.param(
        {"$ref": True},
        {},
        (False, "malformed schema :: The value of $ref must be a string. "),
        id="type $ref not string",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {},
        (False, "reference :: 'RefSchema was not found in schemas.' "),
        id="type $ref missing",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "integer"}},
        (True, None),
        id="type $ref",
    ),
    pytest.param(
        {"allOf": True},
        {},
        (False, "malformed schema :: The value of allOf must be a list. "),
        id="type allOf not array",
    ),
    pytest.param(
        {"allOf": [True]},
        {},
        (False, "malformed schema :: The elements of allOf must be dictionaries. "),
        id="type allOf elements not dict",
    ),
    pytest.param({"allOf": [{"type": "integer"}]}, {}, (True, None), id="type allOf"),
    pytest.param(
        {"type": "integer", "x-json": "True"},
        {},
        (False, "malformed schema :: The x-json property must be of type boolean. "),
        id="x-json invalid",
    ),
    pytest.param({"type": "integer", "x-json": True}, {}, (True, None), id="x-json"),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "integer", "x-json": "True"}},
        (False, "malformed schema :: The x-json property must be of type boolean. "),
        id="x-json invalid $ref",
    ),
    pytest.param(
        {"allOf": [{"type": "integer", "x-json": "True"}]},
        {},
        (False, "malformed schema :: The x-json property must be of type boolean. "),
        id="x-json allOf",
    ),
    pytest.param(
        {"type": "integer", "readOnly": "True"},
        {},
        (False, "malformed schema :: A readOnly property must be of type boolean. "),
        id="readOnly invalid",
    ),
    pytest.param(
        {"type": "integer", "readOnly": True}, {}, (True, None), id="readOnly"
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "integer", "readOnly": "True"}},
        (False, "malformed schema :: A readOnly property must be of type boolean. "),
        id="readOnly invalid $ref",
    ),
    pytest.param(
        {"allOf": [{"type": "integer", "readOnly": "True"}]},
        {},
        (False, "malformed schema :: A readOnly property must be of type boolean. "),
        id="readOnly allOf",
    ),
    pytest.param(
        {"type": "integer", "writeOnly": "True"},
        {},
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="writeOnly invalid",
    ),
    pytest.param(
        {"type": "integer", "writeOnly": True}, {}, (True, None), id="writeOnly"
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "integer", "writeOnly": "True"}},
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="writeOnly invalid $ref",
    ),
    pytest.param(
        {"allOf": [{"type": "integer", "writeOnly": "True"}]},
        {},
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="writeOnly allOf",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_result", CHECK_TYPE_TESTS)
@pytest.mark.schemas
def test_check_type(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check_type is called with the schema and schemas
    THEN the expected result is returned.
    """
    returned_result = property_.check_type(schema=schema, schemas=schemas)

    assert returned_result == expected_result


CHECK_TESTS = [
    pytest.param(
        "prop_1",
        True,
        {},
        {},
        (False, "malformed schema :: The schema must be a dictionary. "),
        id="type check fail",
    ),
    pytest.param(
        "prop_1",
        {"type": "integer", "format": True},
        {},
        {},
        (False, "malformed schema :: A format value must be of type string. "),
        id="simple fail",
    ),
    pytest.param("prop_1", {"type": "integer"}, {}, {}, (True, None), id="simple pass"),
    pytest.param(
        "prop_1",
        {"readOnly": True, "type": "integer", "format": "not supported"},
        {},
        {},
        (False, "not supported format is not supported for integer"),
        id="readOnly fail",
    ),
    pytest.param(
        "prop_1",
        {"readOnly": True, "type": "integer"},
        {},
        {},
        (True, None),
        id="readOnly pass",
    ),
    pytest.param(
        "prop_1",
        {"x-json": True, "type": "integer", "x-index": "True"},
        {},
        {},
        (False, "malformed schema :: A index value must be of type boolean. "),
        id="JSON fail",
    ),
    pytest.param(
        "prop_1",
        {"x-json": True, "type": "integer"},
        {},
        {},
        (True, None),
        id="JSON pass",
    ),
    pytest.param(
        "prop_1",
        {"type": "object"},
        {},
        {},
        (False, "not a reference to another object"),
        id="relationship fail",
    ),
    pytest.param(
        "schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (True, None),
        id="relationship pass",
    ),
]


@pytest.mark.parametrize(
    "property_name, property_schema, parent_schema, schemas, expected_result",
    CHECK_TESTS,
)
@pytest.mark.schemas
def test_check(property_name, property_schema, parent_schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check is called with the schema and schemas
    THEN the expected result is returned.
    """
    returned_result = property_.check(
        schemas, parent_schema, property_name, property_schema
    )

    assert returned_result == expected_result
