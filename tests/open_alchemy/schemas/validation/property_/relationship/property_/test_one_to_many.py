"""Tests for x-to-many relationship validation."""

import pytest

from open_alchemy.schemas.validation.property_.relationship import property_

TESTS = [
    pytest.param(
        {"type": "array"},
        {},
        (False, "array type properties must define the items schema"),
        id="array no items",
    ),
    pytest.param(
        {"type": "array", "items": {}},
        {},
        (
            False,
            "items property :: malformed schema :: Every property requires a type. ",
        ),
        id="array items no type",
    ),
    pytest.param(
        {"type": "array", "items": {"type": True}},
        {},
        (
            False,
            "items property :: malformed schema :: A type property "
            "value must be of type string. ",
        ),
        id="array items type not string",
    ),
    pytest.param(
        {"type": "array", "items": {"type": "not object"}},
        {},
        (False, "items property :: type not an object"),
        id="array items type not object",
    ),
    pytest.param(
        {"type": "array", "items": {"type": "array"}},
        {},
        (False, "items property :: type not an object"),
        id="array items type array",
    ),
    pytest.param(
        {"type": "array", "items": {"type": "object"}},
        {},
        (False, "items property :: not a reference to another object"),
        id="array items no $ref",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": True}},
        {},
        (
            False,
            "items property :: malformed schema :: The value of $ref must be a "
            "string. ",
        ),
        id="array items no $ref not string",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object"}},
        (False, "items property :: referenced schema not constructable"),
        id="array items no $ref not constructable",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {},
        (
            False,
            "items property :: reference :: 'RefSchema was not found in schemas.' ",
        ),
        id="array items no $ref not linked",
    ),
    pytest.param(
        {
            "type": "array",
            "x-json": True,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "property is JSON"),
        id="one to many JSON",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-json": True, "x-tablename": "ref_schema"}},
        (False, "items property :: property is JSON"),
        id="one to many JSON",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many $ref",
    ),
    pytest.param(
        {
            "description": True,
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "malformed schema :: A description value must be of type string. "),
        id="one to many malformed description",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "description": True,
                "type": "array",
                "items": {"$ref": "#/components/schemas/RefRefSchema"},
            },
            "RefRefSchema": {"type": "object", "x-tablename": "ref_schema"},
        },
        (False, "malformed schema :: A description value must be of type string. "),
        id="one to many malformed description $ref",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "description": True,
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                }
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "malformed schema :: A description value must be of type string. "),
        id="one to many malformed description allOf",
    ),
    pytest.param(
        {
            "description": "description 1",
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many $ref",
    ),
    pytest.param(
        {
            "writeOnly": "True",
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="one to many malformed writeOnly",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "writeOnly": "True",
                "type": "array",
                "items": {"$ref": "#/components/schemas/RefRefSchema"},
            },
            "RefRefSchema": {"type": "object", "x-tablename": "ref_schema"},
        },
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="one to many malformed writeOnly $ref",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "writeOnly": "True",
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                }
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="one to many malformed writeOnly allOf",
    ),
    pytest.param(
        {
            "writeOnly": True,
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many $ref",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "type": "array",
                    "x-json": False,
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                },
                {"$ref": "#/components/schemas/RefOtherSchema"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "reference :: 'RefOtherSchema was not found in schemas.' "),
        id="one to many allOf $ref fail",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-json": False, "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many $ref JSON False",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/ArraySchema"},
        {
            "ArraySchema": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/RefSchema"},
            },
            "RefSchema": {"type": "object", "x-tablename": "ref_schema"},
        },
        (True, None),
        id="$ref one to many $ref",
    ),
    pytest.param(
        {
            "allOf": [
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="allOf one to many $ref",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many allOf",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"nullable": False},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many allOf nullable False",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"nullable": "True"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "malformed schema :: A nullable value must be of type boolean. "),
        id="one to many allOf nullable not bool",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"nullable": True},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-to-many relationships are not nullable"),
        id="one to many allOf nullable True",
    ),
    pytest.param(
        {
            "allOf": [
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
            ]
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "nullable": True,
            }
        },
        (False, "x-to-many relationships are not nullable"),
        id="allOf one to many $ref nullable True",
    ),
    pytest.param(
        {
            "type": "array",
            "x-backref": "schema",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (
            False,
            "x-backref cannot be defined on x-to-many relationship property root",
        ),
        id="one to many backref on root",
    ),
    pytest.param(
        {
            "type": "array",
            "x-backref": True,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (
            False,
            "x-backref cannot be defined on x-to-many relationship property root",
        ),
        id="one to many backref on root not string",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-backref": "schema",
            }
        },
        (True, None),
        id="one to many backref $ref",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-backref": True,
            }
        },
        (
            False,
            "items property :: malformed schema :: The x-backref property must be of "
            "type string. ",
        ),
        id="one to many backref $ref not string",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many backref allOf",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                    {"x-backref": "ref_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "items property :: multiple x-backref defined in allOf"),
        id="one to many backref allOf multiple",
    ),
    pytest.param(
        {
            "type": "array",
            "x-foreign-key-column": "id",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (
            False,
            "x-foreign-key-column cannot be defined on x-to-many relationship "
            "property root",
        ),
        id="one to many foreign-key-column on root",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-foreign-key-column": "id",
            }
        },
        (True, None),
        id="one to many foreign-key-column $ref",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-foreign-key-column": True,
            }
        },
        (
            False,
            "items property :: malformed schema :: The x-foreign-key-column property "
            "must be of type string. ",
        ),
        id="one to many foreign-key-column $ref not string",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "id"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many foreign-key-column allOf",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "id"},
                    {"x-foreign-key-column": "name"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "items property :: multiple x-foreign-key-column defined in allOf"),
        id="one to many foreign-key-column allOf multiple",
    ),
    pytest.param(
        {
            "type": "array",
            "x-kwargs": {"key": "value"},
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (
            False,
            "x-kwargs cannot be defined on x-to-many relationship property root",
        ),
        id="one to many kwargs on root",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"key": "value"}},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many allOf kwargs",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"key_1": "value: 1"}},
                    {"x-kwargs": {"key_2": "value: 2"}},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "items property :: multiple x-kwargs defined in allOf"),
        id="one to many allOf kwargs multiple",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": "value"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (
            False,
            "items property :: malformed schema :: The x-kwargs property must be of "
            "type dict. ",
        ),
        id="one to many allOf kwargs key not dict",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"backref": "schema"}},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "items property :: x-kwargs may not contain the backref key"),
        id="one to many allOf kwargs has backref",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"secondary": "schema_ref_schema"}},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "items property :: x-kwargs may not contain the secondary key"),
        id="one to many allOf kwargs has secondary",
    ),
    pytest.param(
        {
            "type": "array",
            "x-uselist": True,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (
            False,
            "x-uselist cannot be defined on x-to-many relationship property root",
        ),
        id="one to many uselist on root",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-uselist": "True",
            }
        },
        (False, "malformed schema :: The x-uselist property must be of type boolean. "),
        id="one to many $ref uselist not boolean",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-uselist": True,
            }
        },
        (True, None),
        id="one to many $ref uselist True",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-uselist": False,
            }
        },
        (False, "x-to-many relationships do not support x-uselist False"),
        id="one to many $ref uselist False",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": True},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many allOf uselist True",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-to-many relationships do not support x-uselist False"),
        id="one to many allOf uselist False",
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
