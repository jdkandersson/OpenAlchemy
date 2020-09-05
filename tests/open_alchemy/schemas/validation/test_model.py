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
        (False, "malformed schema :: The value of $ref must be a string. "),
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
        {},
        {},
        (False, "every model must define x-tablename"),
        id="no tablename",
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
        (False, "properties :: models must have at least 1 property themself"),
        id="no properties",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": True},
        {},
        (False, "properties :: value of properties must be a dictionary"),
        id="properties not dict",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": {}},
        {},
        (False, "properties :: models must have at least 1 property themself"),
        id="properties empty",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": {True: "value"}},
        {},
        (False, "properties :: property names must be strings, True is not"),
        id="properties single key not string",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": {"key": {}}},
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
                "properties": {"key": {}},
            }
        },
        (True, None),
        id="$ref properties single",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-tablename": "schema", "type": "object", "properties": {"key": {}}}
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
                "properties": {"key": {}},
            }
        },
        (False, "properties :: models must have at least 1 property themself"),
        id="properties single on joined table inheritance",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-tablename": "schema",
                    "x-inherits": True,
                    "type": "object",
                    "properties": {"key": {}},
                },
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"key": {}},
            }
        },
        (True, None),
        id="properties multiple on joined table inheritance",
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
                "properties": {"key": {}},
            }
        },
        (False, "properties :: models must have at least 1 property themself"),
        id="properties single on single table inheritance",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-inherits": True, "type": "object", "properties": {"key": {}}},
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"key": {}},
            }
        },
        (True, None),
        id="properties multiple on single table inheritance",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
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
            "properties": {"key": {}},
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
                    "properties": {"key": {}},
                    "required": True,
                },
                {
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": {}},
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
                    "properties": {"key": {}},
                    "required": [],
                },
                {
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": {}},
                    "required": True,
                },
            ]
        },
        {},
        (False, "value of required must be a list"),
        id="multiple required second not list",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
            "required": [True],
        },
        {},
        (False, "required :: all items must be strings"),
        id="required single element not string",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
            "required": [True, "value 2"],
        },
        {},
        (False, "required :: all items must be strings"),
        id="required multiple element first not string",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
            "required": ["value 1", True],
        },
        {},
        (False, "required :: all items must be strings"),
        id="required multiple element second not string",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
            "required": ["not a property"],
        },
        {},
        (False, "required :: all items must be properties, not a property is not"),
        id="required has elements not in properties",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
            "required": ["not a property", "key"],
        },
        {},
        (False, "required :: all items must be properties, not a property is not"),
        id="required has multiple elements first not in properties",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
            "required": ["key", "not a property"],
        },
        {},
        (False, "required :: all items must be properties, not a property is not"),
        id="required has multiple elements second not in properties",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
            "required": ["key"],
        },
        {},
        (True, None),
        id="required has elements not in properties",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-inherits": True,
                    "type": "object",
                    "required": ["parent_key"],
                    "properties": {"key": {}},
                },
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"parent_key": {}},
            }
        },
        (False, "required :: all items must be properties, parent_key is not"),
        id="required property on parent model in single table inheritance",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "type": "object",
                    "required": ["parent_key"],
                    "properties": {"key": {}},
                },
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"parent_key": {}},
            }
        },
        (True, None),
        id="required similar to single table inheritance without inheritance",
    ),
    pytest.param(
        {
            "description": True,
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "malformed schema :: A description value must be of type string. "),
        id="description not string",
    ),
    pytest.param(
        {
            "description": "description 1",
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (True, None),
        id="description string",
    ),
    pytest.param(
        {
            "x-mixins": True,
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (
            False,
            'extension property :: The value of the "x-mixins" extension property is '
            'not valid. The expected schema is {"description": "The import path for a '
            'mixin class to be added as a parent for a model.", "$ref": "#/Mixins"}. '
            "The given value is true. ",
        ),
        id="x-mixins not string",
    ),
    pytest.param(
        {
            "mixins": "mixin.class",
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (True, None),
        id="x-mixins string",
    ),
    pytest.param(
        {
            "x-kwargs": True,
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "malformed schema :: The x-kwargs property must be of type dict. "),
        id="kwargs not dict",
    ),
    pytest.param(
        {
            "x-kwargs": {},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (True, None),
        id="kwargs dict",
    ),
    pytest.param(
        {
            "x-kwargs": {"tablename": True},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models x-kwargs must have keys that start and end with __"),
        id="kwargs dict has tablename",
    ),
    pytest.param(
        {
            "x-kwargs": {"__table_args__": True},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models x-kwargs cannot define __table_args__"),
        id="kwargs dict has __table_args__",
    ),
    pytest.param(
        {
            "x-kwargs": {"arg__": True},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models x-kwargs must have keys that start and end with __"),
        id="kwargs single not start with __",
    ),
    pytest.param(
        {
            "x-kwargs": {"__arg": True},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models x-kwargs must have keys that start and end with __"),
        id="kwargs single not ends with __",
    ),
    pytest.param(
        {
            "x-kwargs": {"__arg__": True},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (True, None),
        id="kwargs single",
    ),
    pytest.param(
        {
            "x-kwargs": {"arg1": True, "__arg2__": False},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models x-kwargs must have keys that start and end with __"),
        id="kwargs multiple first not valid",
    ),
    pytest.param(
        {
            "x-kwargs": {"__arg1__": True, "arg2": False},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models x-kwargs must have keys that start and end with __"),
        id="kwargs multiple second not valid",
    ),
    pytest.param(
        {
            "x-kwargs": {"__arg1__": True, "__arg2__": False},
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (True, None),
        id="kwargs multiple",
    ),
    pytest.param(
        {
            "x-primary-key": "True",
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models do not support the x-primary-key key"),
        id="has x-primary-key invalid",
    ),
    pytest.param(
        {
            "x-primary-key": True,
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models do not support the x-primary-key key"),
        id="has x-primary-key valid",
    ),
    pytest.param(
        {
            "x-autoincrement": "True",
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models do not support the x-autoincrement key"),
        id="has x-autoincrement",
    ),
    pytest.param(
        {
            "x-index": "True",
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models do not support the x-index key"),
        id="has x-index",
    ),
    pytest.param(
        {
            "x-unique": "True",
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models do not support the x-unique key"),
        id="has x-unique",
    ),
    pytest.param(
        {
            "x-foreign-key": True,
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models do not support the x-foreign-key key"),
        id="has x-foreign-key",
    ),
    pytest.param(
        {
            "x-foreign-key-kwargs": True,
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (False, "models do not support the x-foreign-key-kwargs key"),
        id="has x-foreign-key-kwargs",
    ),
    pytest.param(
        {
            "x-composite-index": True,
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (
            False,
            'extension property :: The value of the "x-composite-index" extension '
            'property is not valid. The expected schema is {"description": "Add '
            'composite index to a table.", "$ref": "#/CompositeIndex"}. The given '
            "value is true. ",
        ),
        id="x-composite-index invalid",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-composite-index": True,
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": {}},
                }
            ]
        },
        {},
        (
            False,
            'extension property :: The value of the "x-composite-index" extension '
            'property is not valid. The expected schema is {"description": "Add '
            'composite index to a table.", "$ref": "#/CompositeIndex"}. The given '
            "value is true. ",
        ),
        id="allOf x-composite-index invalid",
    ),
    pytest.param(
        {
            "x-composite-index": ["key"],
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (True, None),
        id="x-composite-index",
    ),
    pytest.param(
        {
            "x-composite-index": ["not a key"],
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (
            False,
            "x-composite-index :: all expressions must be properties, not a key is not",
        ),
        id="x-composite-index column not in properties",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-composite-index": ["parent_key"],
                    "x-inherits": True,
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": {}},
                },
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"parent_key": {}},
            }
        },
        (
            False,
            "x-composite-index :: all expressions must be properties, parent_key is "
            "not",
        ),
        id="x-composite-index column in parent joined table inheritance",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-composite-index": ["parent_key"],
                    "x-inherits": True,
                    "type": "object",
                    "properties": {"key": {}},
                },
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"parent_key": {}},
            }
        },
        (True, None),
        id="x-composite-index column in parent single table inheritance",
    ),
    pytest.param(
        {
            "x-composite-unique": True,
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (
            False,
            'extension property :: The value of the "x-composite-unique" extension '
            'property is not valid. The expected schema is {"description": "Add '
            'composite unique constraint to a table.", "$ref": "#/CompositeUnique"}. '
            "The given value is true. ",
        ),
        id="x-composite-unique invalid",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-composite-unique": True,
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": {}},
                }
            ]
        },
        {},
        (
            False,
            'extension property :: The value of the "x-composite-unique" extension '
            'property is not valid. The expected schema is {"description": "Add '
            'composite unique constraint to a table.", "$ref": "#/CompositeUnique"}. '
            "The given value is true. ",
        ),
        id="allOf x-composite-unique invalid",
    ),
    pytest.param(
        {
            "x-composite-unique": ["key"],
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (True, None),
        id="x-composite-unique",
    ),
    pytest.param(
        {
            "x-composite-unique": ["not a key"],
            "x-tablename": "schema",
            "type": "object",
            "properties": {"key": {}},
        },
        {},
        (
            False,
            "x-composite-unique :: all columns must be properties, not a key is not",
        ),
        id="x-composite-unique column not in properties",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-composite-unique": ["parent_key"],
                    "x-inherits": True,
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"key": {}},
                },
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"parent_key": {}},
            }
        },
        (
            False,
            "x-composite-unique :: all columns must be properties, parent_key is not",
        ),
        id="x-composite-unique column in parent joined table inheritance",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-composite-unique": ["parent_key"],
                    "x-inherits": True,
                    "type": "object",
                    "properties": {"key": {}},
                },
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"parent_key": {}},
            }
        },
        (True, None),
        id="x-composite-unique column in parent single table inheritance",
    ),
]


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    TESTS,
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
