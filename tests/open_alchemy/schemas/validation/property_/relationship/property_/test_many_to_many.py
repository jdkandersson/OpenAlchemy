"""Tests for many-to-many relationship validation."""

import pytest

from open_alchemy.schemas.validation.property_.relationship import property_

TESTS = [
    pytest.param(
        {
            "type": "array",
            "x-json": True,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "property is JSON"),
        id="many to many JSON",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-json": True,
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "items property :: property is JSON"),
        id="many to many $ref JSON",
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
        {
            "description": True,
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "malformed schema :: A description value must be of type string. "),
        id="many to many $ref malformed description",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "description": True,
                "type": "array",
                "items": {"$ref": "#/components/schemas/RefRefSchema"},
            },
            "RefRefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            },
        },
        (False, "malformed schema :: A description value must be of type string. "),
        id="many to many $ref malformed description",
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
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "malformed schema :: A description value must be of type string. "),
        id="many to many $ref malformed description allOf",
    ),
    pytest.param(
        {
            "description": "description 1",
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (True, None),
        id="many to many $ref description",
    ),
    pytest.param(
        {
            "writeOnly": "True",
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="many to many $ref malformed writeOnly",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "writeOnly": "True",
                "type": "array",
                "items": {"$ref": "#/components/schemas/RefRefSchema"},
            },
            "RefRefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            },
        },
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="many to many $ref malformed writeOnly",
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
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="many to many $ref malformed writeOnly allOf",
    ),
    pytest.param(
        {
            "writeOnly": True,
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (True, None),
        id="many to many $ref writeOnly",
    ),
    pytest.param(
        {
            "type": "array",
            "x-json": False,
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {
            "RefSchema": {
                "type": "object",
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (True, None),
        id="many to many JSON False $ref",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-json": False,
                "x-tablename": "ref_schema",
                "x-secondary": "schema_ref_schema",
            }
        },
        (True, None),
        id="many to many $ref JSON False ",
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
        (
            False,
            "malformed schema :: The x-secondary property must be of type string. ",
        ),
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
        (False, "malformed schema :: A nullable value must be of type boolean. "),
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
        (False, "items property :: multiple x-secondary defined in allOf"),
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
        (
            False,
            "x-backref cannot be defined on x-to-many relationship property root",
        ),
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
        (
            False,
            "items property :: malformed schema :: The x-backref property must be of "
            "type string. ",
        ),
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
        (False, "items property :: multiple x-backref defined in allOf"),
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
        id="many to many foreign-key-column on root",
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
        id="many to many foreign-key-column on root not string",
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
        (
            False,
            "items property :: malformed schema :: The x-foreign-key-column property "
            "must be of type string. ",
        ),
        id="many to many $ref foreign-key-column not string",
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
        id="many to many $ref foreign-key-column",
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
        id="many to many foreign-key-column allOf",
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
        (
            False,
            "x-kwargs cannot be defined on x-to-many relationship property root",
        ),
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
        (
            False,
            "x-kwargs cannot be defined on x-to-many relationship property root",
        ),
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
        (False, "items property :: multiple x-kwargs defined in allOf"),
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
        (
            False,
            "items property :: malformed schema :: The x-kwargs property must be of "
            "type dict. ",
        ),
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
        (False, "items property :: x-kwargs may not contain the backref key"),
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
        (False, "items property :: x-kwargs may not contain the secondary key"),
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
        (
            False,
            "x-uselist cannot be defined on x-to-many relationship property root",
        ),
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
        (
            False,
            "x-uselist cannot be defined on x-to-many relationship property root",
        ),
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
        (False, "malformed schema :: The x-uselist property must be of type boolean. "),
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
    pytest.param(
        {
            "allOf": [
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
                {"$ref": "#/components/schemas/RefRefSchema"},
            ]
        },
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        (False, "reference :: 'RefRefSchema was not found in schemas.' "),
        id="many to many allOf $ref not for type no resolve",
    ),
]


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    TESTS,
)
@pytest.mark.schemas
@pytest.mark.validation
def test_check(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check is called with the schemas and schema
    THEN the expected result is returned.
    """
    returned_result = property_.check(schemas, schema)

    assert returned_result == expected_result
