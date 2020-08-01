"""Tests for x-to-many relationship validation."""

import pytest

from open_alchemy.schemas.validation.relationship import property_

TESTS = [
    pytest.param({}, {}, (False, "type not defined"), id="no type"),
    pytest.param(
        {"type": "not relationship"},
        {},
        (False, "type not an object nor array"),
        id="not object nor array type",
    ),
    pytest.param(
        {"type": True},
        {},
        (False, "value of type must be a string"),
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