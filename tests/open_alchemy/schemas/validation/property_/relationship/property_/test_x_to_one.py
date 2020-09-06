"""Tests for x-to-many relationship validation."""

import pytest

from open_alchemy.schemas.validation.property_.relationship import property_

TESTS = [
    pytest.param(
        {},
        {},
        (
            False,
            "malformed schema :: Every property requires a type. ",
        ),
        id="no type",
    ),
    pytest.param(
        {"type": "not relationship"},
        {},
        (False, "type not an object nor array"),
        id="not object nor array type",
    ),
    pytest.param(
        {"type": True},
        {},
        (
            False,
            "malformed schema :: A type property value must be of type string. ",
        ),
        id="type not a string",
    ),
    pytest.param(
        {"type": "object"},
        {},
        (False, "not a reference to another object"),
        id="not object no $ref",
    ),
    pytest.param(
        {"$ref": True},
        {},
        (
            False,
            "malformed schema :: The value of $ref must be a string. ",
        ),
        id="$ref not string",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {},
        (False, "reference :: 'RefSchema was not found in schemas.' "),
        id="$ref not resolve",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        (False, "referenced schema not constructable"),
        id="object $ref not constructable",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema", "x-json": True}},
        (False, "property is JSON"),
        id="many to one $ref JSON",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one $ref",
    ),
    pytest.param(
        {"allOf": True},
        {},
        (
            False,
            "malformed schema :: The value of allOf must be a list. ",
        ),
        id="many to one allOf",
    ),
    pytest.param(
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one allOf",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema1"},
                {"$ref": "#/components/schemas/RefSchema2"},
            ]
        },
        {
            "RefSchema1": {"type": "object", "x-tablename": "ref_schema_1"},
            "RefSchema2": {"type": "object", "x-tablename": "ref_schema_2"},
        },
        (False, "multiple $ref defined in allOf"),
        id="many to one allOf multiple $ref",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "nullable": True,
            }
        },
        (True, None),
        id="many to one nullable $ref",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "nullable": "True",
            }
        },
        (False, "malformed schema :: A nullable value must be of type boolean. "),
        id="many to one nullable $ref not bool",
    ),
    pytest.param(
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"nullable": True}]},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one nullable allOf",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"nullable": True},
                {"nullable": False},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "multiple nullable defined in allOf"),
        id="many to one nullable allOf multiple",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "description": "description 1",
            }
        },
        (True, None),
        id="many to one description $ref",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "description": True,
            }
        },
        (False, "malformed schema :: A description value must be of type string. "),
        id="many to one description $ref not string",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"description": "description 1"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one description allOf",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"description": "description 1"},
                {"description": "description 2"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "multiple description defined in allOf"),
        id="many to one description allOf multiple",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "writeOnly": True,
            }
        },
        (True, None),
        id="many to one writeOnly $ref",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "writeOnly": "True",
            }
        },
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="many to one writeOnly $ref not bool",
    ),
    pytest.param(
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"writeOnly": True}]},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one writeOnly allOf",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"writeOnly": True},
                {"writeOnly": False},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "multiple writeOnly defined in allOf"),
        id="many to one writeOnly allOf multiple",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-backref": "schema",
            }
        },
        (True, None),
        id="many to one backref $ref",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-backref": True,
            }
        },
        (False, "malformed schema :: The x-backref property must be of type string. "),
        id="many to one backref $ref not string",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-backref": "schema"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one backref allOf",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-backref": "schema"},
                {"x-backref": "ref_schema"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "multiple x-backref defined in allOf"),
        id="many to one backref allOf multiple",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-foreign-key-column": "id",
            }
        },
        (True, None),
        id="many to one foreign-key-column $ref",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-foreign-key-column": True,
            }
        },
        (
            False,
            "malformed schema :: The x-foreign-key-column property must be of type "
            "string. ",
        ),
        id="many to one foreign-key-column $ref not string",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-foreign-key-column": "id"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one foreign-key-column allOf",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-foreign-key-column": "id"},
                {"x-foreign-key-column": "name"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "multiple x-foreign-key-column defined in allOf"),
        id="many to one foreign-key-column allOf multiple",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-kwargs": {"key": "value"}},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one allOf kwargs",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-kwargs": {"key_1": "value 1"}},
                {"x-kwargs": {"key_2": "value 2"}},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "multiple x-kwargs defined in allOf"),
        id="many to one allOf kwargs multiple",
    ),
    pytest.param(
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"x-kwargs": True}]},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "malformed schema :: The x-kwargs property must be of type dict. "),
        id="many to one allOf kwargs not dict",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-kwargs": {"backref": "schema"}},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-kwargs may not contain the backref key"),
        id="many to one allOf kwargs has backref",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-kwargs": {"secondary": "schema_ref_schema"}},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-kwargs may not contain the secondary key"),
        id="many to one allOf kwargs has secondary",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-uselist": True,
            }
        },
        (True, None),
        id="many to one $ref uselist",
    ),
    pytest.param(
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"x-uselist": True}]},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one allOf uselist",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "allOf": [
                    {"type": "object", "x-tablename": "ref_schema", "x-json": False},
                    {"$ref": "#/components/schemas/RefRefSchema"},
                ]
            }
        },
        (False, "reference :: 'RefRefSchema was not found in schemas.' "),
        id="many to one $ref not for type not resolve",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-uselist": False,
                "x-backref": "schema",
            }
        },
        (True, None),
        id="one to one $ref",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-uselist": False, "x-backref": "schema"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to one allOf",
    ),
    pytest.param(
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"x-uselist": False}]},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "a one-to-one relationship must define a back reference"),
        id="one to one allOf no backref",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-uselist": "False", "x-backref": "schema"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "malformed schema :: The x-uselist property must be of type boolean. "),
        id="one to one allOf uselist not boolean",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-uselist": False, "x-backref": "schema"},
                {"x-uselist": True},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "multiple x-uselist defined in allOf"),
        id="one to one allOf multiple uselist",
    ),
]


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    TESTS,
)
@pytest.mark.validation
@pytest.mark.schemas
def test_check(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check is called with the schemas and schema
    THEN the expected result is returned.
    """
    returned_result = property_.check(schemas, schema)

    assert returned_result == expected_result
