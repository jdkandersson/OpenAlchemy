"""Tests for relationship validation."""

# pylint: disable=too-many-lines

import pytest

from open_alchemy.schemas.validation import relationship

TESTS = [
    pytest.param(
        {}, {}, (False, "malformed schema when retrieving the type"), id="no type"
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
        (False, "malformed schema when retrieving the type"),
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
        (False, "malformed schema when retrieving the type"),
        id="$ref not string",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {},
        (False, "reference does not resolve"),
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
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one $ref",
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
        (False, "value of nullable must be a boolean"),
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
        (False, "value of x-backref must be a string"),
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
        (False, "value of x-foreign-key-column must be a string"),
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
        (False, "value of x-kwargs must be a dictionary"),
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
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"x-uselist": True},]},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to one allOf uselist",
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
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"x-uselist": False},]},
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
        (False, "value of x-uselist must be a boolean"),
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
    pytest.param(
        {"type": "array"},
        {},
        (False, "array type properties must define the items schema"),
        id="array no items",
    ),
    pytest.param(
        {"type": "array", "items": {}},
        {},
        (False, "value of items malformed schema when retrieving the type"),
        id="array items no type",
    ),
    pytest.param(
        {"type": "array", "items": {"type": True}},
        {},
        (False, "value of items malformed schema when retrieving the type"),
        id="array items type not string",
    ),
    pytest.param(
        {"type": "array", "items": {"type": "not object"}},
        {},
        (False, "value of items type not an object"),
        id="array items type not object",
    ),
    pytest.param(
        {"type": "array", "items": {"type": "array"}},
        {},
        (False, "value of items type not an object"),
        id="array items type array",
    ),
    pytest.param(
        {"type": "array", "items": {"type": "object"}},
        {},
        (False, "value of items not a reference to another object"),
        id="array items no $ref",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": True}},
        {},
        (False, "value of items malformed schema when retrieving the type"),
        id="array items no $ref not string",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object"}},
        (False, "value of items referenced schema not constructable"),
        id="array items no $ref not constructable",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {},
        (False, "value of items reference does not resolve"),
        id="array items no $ref not linked",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="one to many $ref",
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
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"},}
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
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"},}
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
        (False, "x-backref cannot be defined on x-to-many relationship property root",),
        id="one to many backref on root",
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
        (False, "value of items value of x-backref must be a string"),
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
        (False, "value of items multiple x-backref defined in allOf"),
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
        (False, "value of items value of x-foreign-key-column must be a string"),
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
        (False, "value of items multiple x-foreign-key-column defined in allOf"),
        id="one to many foreign-key-column allOf multiple",
    ),
    pytest.param(
        {
            "type": "array",
            "x-kwargs": {"key": "value"},
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-kwargs cannot be defined on x-to-many relationship property root",),
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
        (False, "value of items multiple x-kwargs defined in allOf"),
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
        (False, "value of items value of x-kwargs must be a dictionary"),
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
        (False, "value of items x-kwargs may not contain the backref key"),
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
        (False, "value of items x-kwargs may not contain the secondary key"),
        id="one to many allOf kwargs has secondary",
    ),
    pytest.param(
        {
            "type": "array",
            "x-uselist": True,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-uselist cannot be defined on x-to-many relationship property root",),
        id="one to many uselist on root",
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
        (False, "x-to-many relationship does not support x-uselist False"),
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
        (False, "x-to-many relationship does not support x-uselist False"),
        id="one to many allOf uselist False",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (True, None),
        id="many to many $ref",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": True,
            }
        },
        (False, "value of x-secondary must be a string"),
        id="many to many $ref secondary not string",
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
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to many allOf",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "schema_ref_schema"},
                    {"nullable": False},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to many allOf nullable False",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "schema_ref_schema"},
                    {"nullable": True},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-to-many relationships are not nullable"),
        id="many to many allOf nullable True",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
                "nullable": True,
            }
        },
        (False, "x-to-many relationships are not nullable"),
        id="many to many $ref nullable True",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "schema_ref_schema"},
                    {"x-secondary": "ref_schema_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "value of items multiple x-secondary defined in allOf"),
        id="many to many allOf multiple secondary",
    ),
    pytest.param(
        {
            "type": "array",
            "x-backref": "schema",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "x-backref cannot be defined on x-to-many relationship property root",),
        id="many to many backref on root",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-backref": "schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (True, None),
        id="many to many backref $ref",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-backref": True,
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "value of items value of x-backref must be a string"),
        id="many to many backref $ref not string",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                    {"x-secondary": "schema_ref_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to many backref allOf",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                    {"x-backref": "ref_schema"},
                    {"x-secondary": "schema_ref_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "value of items multiple x-backref defined in allOf"),
        id="many to many backref allOf multiple",
    ),
    pytest.param(
        {
            "type": "array",
            "x-foreign-key-column": "id",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
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
                "x-foreign-key-column": True,
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "value of items value of x-foreign-key-column must be a string"),
        id="one to many $ref foreign-key-column not string",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-foreign-key-column": "id",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "many-to-many relationship does not support x-foreign-key-column"),
        id="one to many $ref foreign-key-column",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "id"},
                    {"x-secondary": "id"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "many-to-many relationship does not support x-foreign-key-column"),
        id="one to many foreign-key-column allOf",
    ),
    pytest.param(
        {
            "type": "array",
            "x-kwargs": {"key": "value"},
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "x-kwargs cannot be defined on x-to-many relationship property root",),
        id="many to many kwargs on root",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"key": "value"}},
                    {"x-secondary": "schema_ref_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to many allOf kwargs",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"key_1": "value 1"}},
                    {"x-kwargs": {"key_2": "value 2"}},
                    {"x-secondary": "schema_ref_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "value of items multiple x-kwargs defined in allOf"),
        id="many to many allOf kwargs multiple",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": "value"},
                    {"x-secondary": "ref_schema_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "value of items value of x-kwargs must be a dictionary"),
        id="many to many allOf kwargs key not dict",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"backref": "schema"}},
                    {"x-secondary": "ref_schema_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "value of items x-kwargs may not contain the backref key"),
        id="many to many allOf kwargs has backref",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"secondary": "schema_ref_schema"}},
                    {"x-secondary": "ref_schema_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "value of items x-kwargs may not contain the secondary key"),
        id="many to many allOf kwargs has secondary",
    ),
    pytest.param(
        {
            "type": "array",
            "x-uselist": True,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "ref_schema_schema",
            }
        },
        (False, "x-uselist cannot be defined on x-to-many relationship property root",),
        id="many to many uselist on root",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-uselist": True,
                "x-secondary": "ref_schema_schema",
            }
        },
        (True, None),
        id="many to many $ref uselist True",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-uselist": False,
                "x-secondary": "ref_schema_schema",
            }
        },
        (False, "x-to-many relationship does not support x-uselist False"),
        id="many to many $ref uselist False",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": True},
                    {"x-secondary": "ref_schema_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (True, None),
        id="many to many allOf uselist True",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False},
                    {"x-secondary": "ref_schema_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-to-many relationship does not support x-uselist False"),
        id="many to many allOf uselist False",
    ),
]


@pytest.mark.parametrize(
    "schema, schemas, expected_result", TESTS,
)
@pytest.mark.schemas
def test_check(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check is called with the schemas and schema
    THEN the expected result is returned.
    """
    returned_result = relationship.check(schemas, schema)

    assert returned_result == expected_result
