"""Tests for x-to-many relationship validation."""

import pytest

from open_alchemy.schemas.validation.relationship import property_

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
        (False, "value of items type not defined"),
        id="array items no type",
    ),
    pytest.param(
        {"type": "array", "items": {"type": True}},
        {},
        (False, "value of items value of type must be a string"),
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
                    {"nullable": "True"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "value of nullable must be a boolean"),
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
        {
            "type": "array",
            "x-backref": True,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "x-backref cannot be defined on x-to-many relationship property root",),
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
                "x-uselist": "True",
            }
        },
        (False, "value of x-uselist must be a boolean"),
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
                    {"nullable": "True"},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "value of nullable must be a boolean"),
        id="many to many allOf nullable not bool",
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
        {
            "type": "array",
            "x-foreign-key-column": True,
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
        id="one to many foreign-key-column on root not string",
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
            "x-secondary": True,
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
            "x-secondary cannot be defined on x-to-many relationship property root",
        ),
        id="many to many kwargs on root not dict",
    ),
    pytest.param(
        {
            "type": "array",
            "x-secondary": "schema_ref_schema",
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
            "x-secondary cannot be defined on x-to-many relationship property root",
        ),
        id="many to many kwargs on root",
    ),
    pytest.param(
        {
            "type": "array",
            "x-kwargs": True,
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
        id="many to many kwargs on root not dict",
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
            "x-uselist": "True",
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
        id="many to many uselist on root not bool",
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
                "x-uselist": "True",
                "x-secondary": "ref_schema_schema",
            }
        },
        (False, "value of x-uselist must be a boolean"),
        id="many to many $ref uselist not boolean",
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
        (False, "x-to-many relationships do not support x-uselist False"),
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
        (False, "x-to-many relationships do not support x-uselist False"),
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
    returned_result = property_.check(schemas, schema)

    assert returned_result == expected_result