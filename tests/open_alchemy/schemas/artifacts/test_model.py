"""Tests for retrieving artifacts of a model."""

import typing

import pytest

from open_alchemy.schemas import artifacts

DEFAULT_SCHEMA: typing.Any = {"x-tablename": "default_table"}
GET_TESTS = [
    pytest.param(
        {**DEFAULT_SCHEMA, "x-tablename": "table_1"},
        {},
        "tablename",
        "table_1",
        id="tablename",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-tablename": "table_2"}},
        "tablename",
        "table_2",
        id="$ref tablename",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "x-tablename": "table_3"}]},
        {},
        "tablename",
        "table_3",
        id="allOf tablename",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-tablename": "local_table"},
            ]
        },
        {"RefSchema": {"x-tablename": "ref_table"}},
        "tablename",
        "local_table",
        id="tablename in $ref and allOf",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "inherits",
        None,
        id="inherits not defined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-inherits": True, "$ref": "#/components/schemas/Parent"},
        {"Parent": {"x-tablename": "parent"}},
        "inherits",
        True,
        id="inherits",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-inherits": False}},
        "inherits",
        False,
        id="$ref inherits",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    **DEFAULT_SCHEMA,
                    "x-inherits": "Parent",
                    "$ref": "#/components/schemas/Parent",
                }
            ]
        },
        {"Parent": {"x-tablename": "parent"}},
        "inherits",
        True,
        id="allOf inherits",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "x-inherits": "Parent",
            "$ref": "#/components/schemas/Parent",
        },
        {"Parent": {"x-tablename": "parent"}},
        "parent",
        "Parent",
        id="parent",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "description",
        None,
        id="description not defined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "description": "description 1"},
        {},
        "description",
        "description 1",
        id="description",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "description": "description 2"}},
        "description",
        "description 2",
        id="$ref description",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "description": "description 3"},
            ]
        },
        {"RefSchema": {"description": "description 4"}},
        "description",
        "description 3",
        id="allOf description",
    ),
    pytest.param({**DEFAULT_SCHEMA}, {}, "mixins", None, id="x-mixins not defined"),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-mixins": "module.Mixin1"},
        {},
        "mixins",
        ["module.Mixin1"],
        id="x-mixins",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-mixins": ["module.Mixin2"]}},
        "mixins",
        ["module.Mixin2"],
        id="$ref x-mixins",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-mixins": ["module.Mixin3", "module.Mixin4"]},
            ]
        },
        {"RefSchema": {"x-mixins": ["module.Mixin5"]}},
        "mixins",
        ["module.Mixin3", "module.Mixin4"],
        id="allOf x-mixins",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "kwargs",
        None,
        id="x-kwargs not defined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-kwargs": {"key_1": "value 1"}},
        {},
        "kwargs",
        {"key_1": "value 1"},
        id="x-kwargs",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-kwargs": {"key_2": "value 2"}}},
        "kwargs",
        {"key_2": "value 2"},
        id="$ref x-kwargs",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-kwargs": {"key_3": "value 3"}},
            ]
        },
        {"RefSchema": {"x-kwargs": {"key_4": "value 4"}}},
        "kwargs",
        {"key_3": "value 3"},
        id="allOf x-kwargs",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "composite_index",
        None,
        id="x-composite-index not defined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-composite-index": ["column_1"]},
        {},
        "composite_index",
        [{"expressions": ["column_1"]}],
        id="x-composite-index",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                **DEFAULT_SCHEMA,
                "x-composite-index": [["column_1"], ["column_2"]],
            }
        },
        "composite_index",
        [{"expressions": ["column_1"]}, {"expressions": ["column_2"]}],
        id="$ref x-composite-index",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {
                    **DEFAULT_SCHEMA,
                    "x-composite-index": [
                        {"name": "index-1", "expressions": ["column_1"]}
                    ],
                },
            ]
        },
        {
            "RefSchema": {
                "x-composite-index": [{"name": "index-2", "expressions": ["column_2"]}]
            }
        },
        "composite_index",
        [{"name": "index-1", "expressions": ["column_1"]}],
        id="allOf x-composite-index",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "composite_unique",
        None,
        id="x-composite-unique not defined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-composite-unique": ["column_1"]},
        {},
        "composite_unique",
        [{"columns": ["column_1"]}],
        id="x-composite-unique",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                **DEFAULT_SCHEMA,
                "x-composite-unique": [["column_1"], ["column_2"]],
            }
        },
        "composite_unique",
        [{"columns": ["column_1"]}, {"columns": ["column_2"]}],
        id="$ref x-composite-unique",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {
                    **DEFAULT_SCHEMA,
                    "x-composite-unique": [
                        {"name": "unique-1", "columns": ["column_1"]}
                    ],
                },
            ]
        },
        {
            "RefSchema": {
                "x-composite-unique": [{"name": "unique-2", "columns": ["column_2"]}]
            }
        },
        "composite_unique",
        [{"name": "unique-1", "columns": ["column_1"]}],
        id="allOf x-composite-unique",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "backrefs",
        [],
        id="backrefs not defined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-backrefs": {}},
        {},
        "backrefs",
        [],
        id="backrefs empty",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "x-backrefs": {"backref_1": {"type": "object", "x-de-$ref": "Parent1"}},
        },
        {},
        "backrefs",
        [("backref_1", ("OBJECT", "Parent1"))],
        id="backrefs single object",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "x-backrefs": {
                "backref_1": {
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "Parent1"},
                }
            },
        },
        {},
        "backrefs",
        [("backref_1", ("ARRAY", "Parent1"))],
        id="backrefs single array",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                **DEFAULT_SCHEMA,
                "x-backrefs": {"backref_1": {"type": "object", "x-de-$ref": "Parent1"}},
            }
        },
        "backrefs",
        [("backref_1", ("OBJECT", "Parent1"))],
        id="$ref backrefs single object",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    **DEFAULT_SCHEMA,
                    "x-backrefs": {
                        "backref_1": {"type": "object", "x-de-$ref": "Parent1"}
                    },
                }
            ]
        },
        {},
        "backrefs",
        [("backref_1", ("OBJECT", "Parent1"))],
        id="allOf backrefs single object",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "x-backrefs": {
                "backref_1": {"type": "object", "x-de-$ref": "Parent1"},
                "backref_2": {"type": "object", "x-de-$ref": "Parent2"},
            },
        },
        {},
        "backrefs",
        [("backref_1", ("OBJECT", "Parent1")), ("backref_2", ("OBJECT", "Parent2"))],
        id="backrefs multiple",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    **DEFAULT_SCHEMA,
                    "x-backrefs": {
                        "backref_1": {"type": "object", "x-de-$ref": "Parent1"}
                    },
                },
                {
                    "type": "object",
                    "x-backrefs": {
                        "backref_2": {"type": "object", "x-de-$ref": "Parent2"}
                    },
                },
            ]
        },
        {},
        "backrefs",
        [("backref_1", ("OBJECT", "Parent1")), ("backref_2", ("OBJECT", "Parent2"))],
        id="backrefs allOf multiple",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    **DEFAULT_SCHEMA,
                    "x-backrefs": {
                        "backref_1": {"type": "object", "x-de-$ref": "Parent1"}
                    },
                },
                {"$ref": "#/components/schemas/RefSchema"},
            ]
        },
        {
            "RefSchema": {
                "type": "object",
                "x-backrefs": {"backref_2": {"type": "object", "x-de-$ref": "Parent2"}},
            }
        },
        "backrefs",
        [("backref_1", ("OBJECT", "Parent1")), ("backref_2", ("OBJECT", "Parent2"))],
        id="backrefs parent and child multiple",
    ),
]


@pytest.mark.parametrize("schema, schemas, key, expected_value", GET_TESTS)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_get(schema, schemas, key, expected_value):
    """
    GIVEN schema, schemas, key and expected value
    WHEN get is called with the schema and schemas
    THEN the returned artifacts has the expected value behind the key.
    """
    returned_artifacts = artifacts.model.get(schemas, schema)

    assert getattr(returned_artifacts, key) == expected_value
