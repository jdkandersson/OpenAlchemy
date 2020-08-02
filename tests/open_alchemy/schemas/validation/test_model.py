"""Tests for validating model schema."""

import pytest

from open_alchemy.schemas.validation import model

TESTS = [
    pytest.param(
        True,
        {},
        (False, "malformed schema :: The schema must be a dictionary. "),
        id="schema not dict",
    ),
    pytest.param(
        {"$ref": True},
        {},
        (False, "malformed schema :: The value of $ref must ba a string. "),
        id="$ref not string",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {},
        (False, "reference :: 'RefSchema was not found in schemas.' "),
        id="$ref not resolve",
    ),
    pytest.param(
        {"allOf": True},
        {},
        (False, "malformed schema :: The value of allOf must be a list. "),
        id="allOf not list",
    ),
    pytest.param(
        {"allOf": [True]},
        {},
        (False, "malformed schema :: The elements of allOf must be dictionaries. "),
        id="allOf elements not dict",
    ),
    pytest.param(
        {}, {}, (False, "every model must define x-tablename"), id="no tablename",
    ),
    pytest.param(
        {"x-tablename": True},
        {},
        (
            False,
            "malformed schema :: The x-tablename property must be of type string. ",
        ),
        id="tablename not string",
    ),
    pytest.param(
        {"x-inherits": 1},
        {},
        (
            False,
            "malformed schema :: The x-inherits property must be of type string or "
            "boolean. ",
        ),
        id="x-inherits MalformedSchemaError",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-inherits": "ParentSchema"},
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {},
        (False, "reference :: 'ParentSchema was not found in schemas.' "),
        id="x-inherits SchemaNotFoundError",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-inherits": "ParentSchema"},
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {"ParentSchema": {}},
        (
            False,
            "malformed schema :: A schema that is marked as inhereting does not "
            "reference a valid parent. ",
        ),
        id="x-inherits parent not constructable",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-inherits": True, "x-tablename": True},
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {"ParentSchema": {"x-tablename": "parent_schema"}},
        (
            False,
            "malformed schema :: The x-tablename property must be of type string. ",
        ),
        id="x-inherits parent not constructable",
    ),
    pytest.param(
        {"x-tablename": "schema"},
        {},
        (False, "malformed schema :: Every property requires a type. "),
        id="no type",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "not object"},
        {},
        (False, "models must have the object type"),
        id="type not object",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object"},
        {},
        (False, "models must have at least 1 property themself"),
        id="no properties",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": True},
        {},
        (False, "models must have at least 1 property themself"),
        id="properties not dict",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": {}},
        {},
        (False, "models must have at least 1 property themself"),
        id="properties empty",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": {"key": "value"}},
        {},
        (True, None),
        id="properties single",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "schema",
                "type": "object",
                "properties": {"key": "value"},
            }
        },
        (True, None),
        id="$ref properties single",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": "value"},
                }
            ]
        },
        {},
        (True, None),
        id="allOf properties single",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-tablename": "schema", "x-inherits": True, "type": "object"},
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"key": "value"},
            }
        },
        (False, "models must have at least 1 property themself"),
        id="properties single on joined table inheritance",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-inherits": True, "type": "object"},
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"key": "value"},
            }
        },
        (False, "models must have at least 1 property themself"),
        id="properties single on single table inheritance",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": "value"},
            "required": True,
        },
        {},
        (False, "value of required must be a list"),
        id="required not list",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": "value"},
            "required": [],
        },
        {},
        (True, None),
        id="required",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": "value"},
                    "required": True,
                },
                {
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": "value"},
                    "required": [],
                },
            ]
        },
        {},
        (False, "value of required must be a list"),
        id="multiple required first not list",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": "value"},
                    "required": [],
                },
                {
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": "value"},
                    "required": True,
                },
            ]
        },
        {},
        (False, "value of required must be a list"),
        id="multiple required second not list",
    ),
    # pytest.param(
    #     {
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #         "required": ["not a property"],
    #     },
    #     {},
    #     (False, None),
    #     id="required has elements not in properties",
    # ),
    # pytest.param(
    #     {
    #         "description": True,
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (False, None),
    #     id="description not string",
    # ),
    # pytest.param(
    #     {
    #         "description": "description 1",
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="description string",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": True,
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (False, None),
    #     id="kwargs not dict",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="kwargs dict",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {"tablename": True},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (False, None),
    #     id="kwargs dict has tablename",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {"__table_args__": True},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (False, None),
    #     id="kwargs dict has __table_args__",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {"arg__": True},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (False, None),
    #     id="kwargs single not start with __",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {"__arg": True},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (False, None),
    #     id="kwargs single not ends with __",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {"__arg__": True},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="kwargs single",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {"__arg1": True, "__arg2__": False},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (False, None),
    #     id="kwargs multiple first not valid",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {"__arg1__": True, "arg2__": False},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (False, None),
    #     id="kwargs multiple second not valid",
    # ),
    # pytest.param(
    #     {
    #         "x-kwargs": {"__arg1__": True, "__arg2__": False},
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="kwargs multiple",
    # ),
    # pytest.param(
    #     {
    #         "x-primary-key": "True",
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="has x-primary-key",
    # ),
    # pytest.param(
    #     {
    #         "x-autoincrement": "True",
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="has x-autoincrement",
    # ),
    # pytest.param(
    #     {
    #         "x-index": "True",
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="has x-index",
    # ),
    # pytest.param(
    #     {
    #         "x-unique": "True",
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="has x-unique",
    # ),
    # pytest.param(
    #     {
    #         "x-foreign-key": True,
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="has x-foreign-key",
    # ),
    # pytest.param(
    #     {
    #         "x-foreign-key-kwargs": True,
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="has x-foreign-key-kwargs",
    # ),
    # pytest.param(
    #     {
    #         "x-composite-index": True,
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="x-composite-index invalid",
    # ),
    # pytest.param(
    #     {
    #         "x-composite-index": [],
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="x-composite-index",
    # ),
    # pytest.param(
    #     {
    #         "x-composite-unique": True,
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="x-composite-unique invalid",
    # ),
    # pytest.param(
    #     {
    #         "x-composite-unique": [],
    #         "x-tablename": "schema",
    #         "type": "object",
    #         "properties": {"key": "value"},
    #     },
    #     {},
    #     (True, None),
    #     id="x-composite-unique",
    # ),
]


@pytest.mark.parametrize(
    "schema, schemas, expected_result", TESTS,
)
@pytest.mark.schemas
def test_check(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check is called with the schema and schemas
    THEN the expected result is returned.
    """
    returned_result = model.check(schemas, schema)

    assert returned_result == expected_result
