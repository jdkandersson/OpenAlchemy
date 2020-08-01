"""Tests for simple property validator pre-processor."""

import pytest

from open_alchemy.schemas.validation import simple

TESTS = [
    pytest.param({}, {}, (False, "must define a type"), id="type missing",),
    pytest.param(
        {"type": True},
        {},
        (False, "value of type must be of type string"),
        id="type not a string",
    ),
    pytest.param(
        {"type": "not supported"},
        {},
        (False, "not supported type is not supported"),
        id="type not supported",
    ),
    pytest.param(
        {"type": "object"},
        {},
        (False, "object type is not supported"),
        id="type object",
    ),
    pytest.param(
        {"type": "array"}, {}, (False, "array type is not supported"), id="type array",
    ),
    pytest.param({"type": "integer"}, {}, (True, None), id="type integer",),
    pytest.param(
        {"$ref": True},
        {},
        (False, "value of $ref must be a string"),
        id="$ref not string",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {},
        (False, "could not resolve reference"),
        id="type integer $ref",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "integer"}},
        (True, None),
        id="type integer $ref",
    ),
    pytest.param(
        {"allOf": True},
        {},
        (False, "value of allOf must be a list"),
        id="allOf not list",
    ),
    pytest.param(
        {"allOf": [True]},
        {},
        (False, "value of allOf must have dictionary elements"),
        id="allOf element not dictionary",
    ),
    pytest.param(
        {"allOf": [{"type": "integer"}]}, {}, (True, None), id="type integer allOf",
    ),
    pytest.param({"type": "number"}, {}, (True, None), id="type number",),
    pytest.param({"type": "boolean"}, {}, (True, None), id="type boolean",),
    pytest.param(
        {"type": "integer", "format": True},
        {},
        (False, "value of format must be of type string"),
        id="format not string",
    ),
    pytest.param(
        {"type": "integer", "format": "unsupported"},
        {},
        (False, "unsupported format is not supported for integer"),
        id="integer format unsupported",
    ),
    pytest.param(
        {"type": "integer", "format": "int32"},
        {},
        (True, None),
        id="integer format int32",
    ),
    pytest.param(
        {"type": "integer", "format": "int64"},
        {},
        (True, None),
        id="integer format int64",
    ),
    pytest.param(
        {"type": "number", "format": "unsupported"},
        {},
        (False, "unsupported format is not supported for number"),
        id="number format unsupported",
    ),
    pytest.param(
        {"type": "number", "format": "float"},
        {},
        (True, None),
        id="number format float",
    ),
    pytest.param(
        {"type": "string", "format": "unsupported"},
        {},
        (False, "unsupported format is not supported for string"),
        id="string format unsupported",
    ),
    pytest.param(
        {"type": "string", "format": "password"},
        {},
        (True, None),
        id="string format password",
    ),
    pytest.param(
        {"type": "string", "format": "byte"}, {}, (True, None), id="string format byte",
    ),
    pytest.param(
        {"type": "string", "format": "binary"},
        {},
        (True, None),
        id="string format binary",
    ),
    pytest.param(
        {"type": "string", "format": "date"}, {}, (True, None), id="string format date",
    ),
    pytest.param(
        {"type": "string", "format": "date-time"},
        {},
        (True, None),
        id="string format date-time",
    ),
    pytest.param(
        {"type": "boolean", "format": ""},
        {},
        (True, None),
        id="boolean does not support format",
    ),
    pytest.param(
        {"type": "string", "maxLength": "1"},
        {},
        (False, "value of maxLength must be an integer"),
        id="string maxLength not integer",
    ),
    pytest.param(
        {"type": "string", "maxLength": 1}, {}, (True, None), id="string maxLength",
    ),
    pytest.param(
        {"type": "string", "format": "date", "maxLength": 1},
        {},
        (False, "string date format does not support maxLength"),
        id="string maxLength format date",
    ),
    pytest.param(
        {"type": "string", "format": "date-time", "maxLength": 1},
        {},
        (False, "string date-time format does not support maxLength"),
        id="string maxLength format date-time",
    ),
    pytest.param(
        {"type": "integer", "maxLength": 1},
        {},
        (False, "integer does not support maxLength"),
        id="integer maxLength",
    ),
    pytest.param(
        {"type": "number", "maxLength": 1},
        {},
        (False, "number does not support maxLength"),
        id="number maxLength",
    ),
    pytest.param(
        {"type": "boolean", "maxLength": 1},
        {},
        (False, "boolean does not support maxLength"),
        id="boolean maxLength",
    ),
    pytest.param(
        {"type": "integer", "nullable": "True"},
        {},
        (False, "value of nullable must be of type boolean"),
        id="integer nullable not boolean",
    ),
    pytest.param(
        {"type": "integer", "nullable": True}, {}, (True, None), id="integer nullable",
    ),
    pytest.param(
        {"type": "number", "nullable": True}, {}, (True, None), id="number nullable",
    ),
    pytest.param(
        {"type": "string", "nullable": True}, {}, (True, None), id="string nullable",
    ),
    pytest.param(
        {"type": "boolean", "nullable": True}, {}, (True, None), id="boolean nullable",
    ),
    pytest.param(
        {"type": "integer", "description": True},
        {},
        (False, "value of description must be of type string"),
        id="integer description not boolean",
    ),
    pytest.param(
        {"type": "integer", "description": "description 1"},
        {},
        (True, None),
        id="integer description",
    ),
    pytest.param(
        {"type": "number", "description": "description 1"},
        {},
        (True, None),
        id="number description",
    ),
    pytest.param(
        {"type": "string", "description": "description 1"},
        {},
        (True, None),
        id="string description",
    ),
    pytest.param(
        {"type": "boolean", "description": "description 1"},
        {},
        (True, None),
        id="boolean description",
    ),
    pytest.param(
        {"type": "integer", "x-primary-key": "True"},
        {},
        (False, "value of x-primary-key must be of type boolean"),
        id="integer x-primary-key not boolean",
    ),
    pytest.param(
        {"type": "integer", "x-primary-key": True},
        {},
        (True, None),
        id="integer x-primary-key",
    ),
    pytest.param(
        {"type": "number", "x-primary-key": True},
        {},
        (True, None),
        id="number x-primary-key",
    ),
    pytest.param(
        {"type": "string", "x-primary-key": True},
        {},
        (True, None),
        id="string x-primary-key",
    ),
    pytest.param(
        {"type": "boolean", "x-primary-key": True},
        {},
        (True, None),
        id="boolean x-primary-key",
    ),
    pytest.param(
        {"type": "integer", "x-autoincrement": "True"},
        {},
        (False, "value of x-autoincrement must be of type boolean"),
        id="integer x-autoincrement not boolean",
    ),
    pytest.param(
        {"type": "integer", "x-autoincrement": True},
        {},
        (True, None),
        id="integer x-autoincrement",
    ),
    pytest.param(
        {"type": "number", "x-autoincrement": True},
        {},
        (False, "number does not support x-autoincrement"),
        id="number x-autoincrement",
    ),
    pytest.param(
        {"type": "string", "x-autoincrement": True},
        {},
        (False, "number does not support x-autoincrement"),
        id="string x-autoincrement",
    ),
    pytest.param(
        {"type": "boolean", "x-autoincrement": True},
        {},
        (False, "number does not support x-autoincrement"),
        id="boolean x-autoincrement",
    ),
    pytest.param(
        {"type": "integer", "x-index": "True"},
        {},
        (False, "value of x-index must be of type boolean"),
        id="integer x-index not boolean",
    ),
    pytest.param(
        {"type": "integer", "x-index": True}, {}, (True, None), id="integer x-index",
    ),
    pytest.param(
        {"type": "number", "x-index": True}, {}, (True, None), id="number x-index",
    ),
    pytest.param(
        {"type": "string", "x-index": True}, {}, (True, None), id="string x-index",
    ),
    pytest.param(
        {"type": "boolean", "x-index": True}, {}, (True, None), id="boolean x-index",
    ),
    pytest.param(
        {"type": "integer", "x-unique": "True"},
        {},
        (False, "value of x-unique must be of type boolean"),
        id="integer x-unique not boolean",
    ),
    pytest.param(
        {"type": "integer", "x-unique": True}, {}, (True, None), id="integer x-unique",
    ),
    pytest.param(
        {"type": "number", "x-unique": True}, {}, (True, None), id="number x-unique",
    ),
    pytest.param(
        {"type": "string", "x-unique": True}, {}, (True, None), id="string x-unique",
    ),
    pytest.param(
        {"type": "boolean", "x-unique": True}, {}, (True, None), id="boolean x-unique",
    ),
    pytest.param(
        {"type": "integer", "x-foreign-key": True},
        {},
        (False, "value of x-foreign-key must be of type string"),
        id="integer x-foreign-key not boolean",
    ),
    pytest.param(
        {"type": "integer", "x-foreign-key": "foreign.key"},
        {},
        (True, None),
        id="integer x-foreign-key",
    ),
    pytest.param(
        {"type": "number", "x-foreign-key": "foreign.key"},
        {},
        (True, None),
        id="number x-foreign-key",
    ),
    pytest.param(
        {"type": "string", "x-foreign-key": "foreign.key"},
        {},
        (True, None),
        id="string x-foreign-key",
    ),
    pytest.param(
        {"type": "boolean", "x-foreign-key": "foreign.key"},
        {},
        (True, None),
        id="boolean x-foreign-key",
    ),
    pytest.param(
        {"type": "integer", "default": True},
        {},
        (False, "the default for an integer must be of type integer"),
        id="integer default invalid",
    ),
    pytest.param(
        {"type": "integer", "default": 1}, {}, (True, None), id="integer default",
    ),
    pytest.param(
        {"type": "number", "default": True},
        {},
        (False, "the default for an number must be of type number"),
        id="number default invalid",
    ),
    pytest.param(
        {"type": "number", "default": 1.1}, {}, (True, None), id="number default",
    ),
    pytest.param(
        {"type": "string", "default": True},
        {},
        (False, "the default for an string must be of type string"),
        id="string default invalid",
    ),
    pytest.param(
        {"type": "string", "default": "value 1"}, {}, (True, None), id="string default",
    ),
    pytest.param(
        {"type": "boolean", "default": "True"},
        {},
        (False, "the default for an boolean must be of type boolean"),
        id="boolean default invalid",
    ),
    pytest.param(
        {"type": "boolean", "default": "value 1"},
        {},
        (True, None),
        id="boolean default",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": 1},
        {},
        (False, "the value of x-kwargs must be a dictionary"),
        id="x-kwargs not dict",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {1: True}},
        {},
        (False, "the keys of x-dict must be a string"),
        id="x-kwargs keys not dict",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {"nullable": True}},
        {},
        (False, "x-kwargs cannot define nullable"),
        id="x-kwargs has nullable",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {"default": 1}},
        {},
        (False, "x-kwargs cannot define default"),
        id="x-kwargs has default",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {"primary_key": True}},
        {},
        (False, "x-kwargs cannot define primary_key"),
        id="x-kwargs has primary_key",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {"autoincrement": True}},
        {},
        (False, "x-kwargs cannot define autoincrement"),
        id="x-kwargs has autoincrement",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {"index": True}},
        {},
        (False, "x-kwargs cannot define index"),
        id="x-kwargs has index",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {"unique": True}},
        {},
        (False, "x-kwargs cannot define unique"),
        id="x-kwargs has unique",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {"key": "value"}},
        {},
        (True, None),
        id="x-kwargs",
    ),
    pytest.param(
        {"type": "integer", "x-foreign-key-kwargs": {"key": "value"}},
        {},
        (False, "the value of x-foreign-key-kwargs must be a dictionary"),
        id="x-foreign-key-kwargs can only be defined alongside x-foreign-key",
    ),
    pytest.param(
        {"type": "integer", "x-foreign-key-kwargs": 1, "x-foreign-key": "foreign.key"},
        {},
        (False, "the value of x-foreign-key-kwargs must be a dictionary"),
        id="x-foreign-key-kwargs not dict",
    ),
    pytest.param(
        {
            "type": "integer",
            "x-foreign-key-kwargs": {1: True},
            "x-foreign-key": "foreign.key",
        },
        {},
        (False, "the keys of x-dict must be a string"),
        id="x-foreign-key-kwargs keys not dict",
    ),
    pytest.param(
        {
            "type": "integer",
            "x-foreign-key-kwargs": {"key": "value"},
            "x-foreign-key": "foreign.key",
        },
        {},
        (True, None),
        id="x-foreign-key-kwargs keys not dict",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_result", TESTS)
@pytest.mark.schemas
def test_check(schema, schemas, expected_result):
    """
    GIVEN schemas, schema and the expected result
    WHEN check is called with the schemas schema
    THEN the expected result is returned.
    """
    # pylint: disable=assignment-from-no-return
    returned_result = simple.check(schemas, schema)

    assert returned_result == expected_result
