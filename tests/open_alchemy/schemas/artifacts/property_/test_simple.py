"""Tests for retrieving artifacts of a simple property."""

import copy
import functools
import typing

import pytest

from open_alchemy.schemas import artifacts
from open_alchemy.schemas.helpers.property_ import type_

DEFAULT_SCHEMA: typing.Any = {"type": "default type"}
GET_TESTS = [
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "type_", type_.Type.SIMPLE, id="property type"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "key": "value"},
        {},
        "schema",
        {**DEFAULT_SCHEMA, "key": "value"},
        id="schema",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "key": "value"}},
        "schema",
        {**DEFAULT_SCHEMA, "key": "value"},
        id="$ref schema",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "key": "value"}]},
        {},
        "schema",
        {**DEFAULT_SCHEMA, "key": "value"},
        id="schema",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "x-primary-key": True,
            "x-index": True,
            "x-unique": True,
            "x-foreign-key": "foreign.key",
            "x-kwargs": {"key": "value"},
            "x-foreign-key-kwargs": {"key": "value"},
        },
        {},
        "schema",
        {**DEFAULT_SCHEMA},
        id="schema remove extension",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "type": "type 1"}, {}, "open_api.type_", "type 1", id="type"
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "type": "type 2"}},
        "open_api.type_",
        "type 2",
        id="$ref type",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "type": "type 3"}]},
        {},
        "open_api.type_",
        "type 3",
        id="allOf type",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "open_api.format_", None, id="format undefined"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "format": "format 1"},
        {},
        "open_api.format_",
        "format 1",
        id="format",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "format": "format 2"}},
        "open_api.format_",
        "format 2",
        id="$ref format",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "format": "format 3"}]},
        {},
        "open_api.format_",
        "format 3",
        id="allOf format",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "open_api.max_length", None, id="maxLength undefined"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "maxLength": 1}, {}, "open_api.max_length", 1, id="maxLength"
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "maxLength": 2}},
        "open_api.max_length",
        2,
        id="$ref maxLength",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "maxLength": 3}]},
        {},
        "open_api.max_length",
        3,
        id="allOf maxLength",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "open_api.nullable", None, id="nullable undefined"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "nullable": True},
        {},
        "open_api.nullable",
        True,
        id="nullable",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "nullable": False}},
        "open_api.nullable",
        False,
        id="$ref nullable",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "nullable": None}]},
        {},
        "open_api.nullable",
        None,
        id="allOf nullable",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "open_api.description", None, id="description undefined"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "description": "description 1"},
        {},
        "open_api.description",
        "description 1",
        id="description",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "description": "description  2"}},
        "open_api.description",
        "description  2",
        id="$ref description",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "description": "description 3"}]},
        {},
        "open_api.description",
        "description 3",
        id="allOf description",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "type": "integer"},
        {},
        "open_api.default",
        None,
        id="default undefined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "type": "integer", "default": 1},
        {},
        "open_api.default",
        1,
        id="default",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "type": "integer", "default": 2}},
        "open_api.default",
        2,
        id="$ref default",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "type": "integer", "default": 3}]},
        {},
        "open_api.default",
        3,
        id="allOf default",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "open_api.read_only", None, id="readOnly undefined"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "readOnly": True},
        {},
        "open_api.read_only",
        True,
        id="readOnly",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "readOnly": False}},
        "open_api.read_only",
        False,
        id="$ref readOnly",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "readOnly": None}]},
        {},
        "open_api.read_only",
        None,
        id="allOf readOnly",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "open_api.write_only", None, id="writeOnly undefined"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "writeOnly": True},
        {},
        "open_api.write_only",
        True,
        id="writeOnly",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "writeOnly": False}},
        "open_api.write_only",
        False,
        id="$ref writeOnly",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "writeOnly": None}]},
        {},
        "open_api.write_only",
        None,
        id="allOf writeOnly",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "extension.primary_key",
        False,
        id="x-primary-key undefined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-primary-key": True},
        {},
        "extension.primary_key",
        True,
        id="x-primary-key",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-primary-key": False}},
        "extension.primary_key",
        False,
        id="$ref x-primary-key",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "x-primary-key": None}]},
        {},
        "extension.primary_key",
        False,
        id="allOf x-primary-key",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "extension.autoincrement",
        None,
        id="x-autoincrement undefined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-autoincrement": True},
        {},
        "extension.autoincrement",
        True,
        id="x-autoincrement",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-autoincrement": False}},
        "extension.autoincrement",
        False,
        id="$ref x-autoincrement",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "x-autoincrement": None}]},
        {},
        "extension.autoincrement",
        None,
        id="allOf x-autoincrement",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "extension.index", None, id="x-index undefined"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-index": True}, {}, "extension.index", True, id="x-index",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-index": False}},
        "extension.index",
        False,
        id="$ref x-index",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "x-index": None}]},
        {},
        "extension.index",
        None,
        id="allOf x-index",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "extension.unique", None, id="x-unique undefined"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-unique": True},
        {},
        "extension.unique",
        True,
        id="x-unique",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-unique": False}},
        "extension.unique",
        False,
        id="$ref x-unique",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "x-unique": None}]},
        {},
        "extension.unique",
        None,
        id="allOf x-unique",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "extension.foreign_key",
        None,
        id="x-foreign-key undefined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-foreign-key": "foreign.key1"},
        {},
        "extension.foreign_key",
        "foreign.key1",
        id="x-foreign-key",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-foreign-key": "foreign.key2"}},
        "extension.foreign_key",
        "foreign.key2",
        id="$ref x-foreign-key",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "x-foreign-key": "foreign.key3"}]},
        {},
        "extension.foreign_key",
        "foreign.key3",
        id="allOf x-foreign-key",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "extension.kwargs", None, id="x-kwargs undefined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-kwargs": {"key_1": "value 1"}},
        {},
        "extension.kwargs",
        {"key_1": "value 1"},
        id="x-kwargs",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-kwargs": {"key_2": "value 2"}}},
        "extension.kwargs",
        {"key_2": "value 2"},
        id="$ref x-kwargs",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "x-kwargs": {"key_3": "value 3"}}]},
        {},
        "extension.kwargs",
        {"key_3": "value 3"},
        id="allOf x-kwargs",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA},
        {},
        "extension.foreign_key_kwargs",
        None,
        id="x-kwargs undefined",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "x-foreign-key-kwargs": {"key_1": "value 1"}},
        {},
        "extension.foreign_key_kwargs",
        {"key_1": "value 1"},
        id="x-foreign-key-kwargs",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-foreign-key-kwargs": {"key_2": "value 2"}}},
        "extension.foreign_key_kwargs",
        {"key_2": "value 2"},
        id="$ref x-foreign-key-kwargs",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "x-foreign-key-kwargs": {"key_3": "value 3"}}]},
        {},
        "extension.foreign_key_kwargs",
        {"key_3": "value 3"},
        id="allOf x-foreign-key-kwargs",
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
    original_schemas = copy.deepcopy(schemas)

    returned_artifacts = artifacts.property_.simple.get(schemas, schema)

    value = functools.reduce(getattr, key.split("."), returned_artifacts)
    assert value == expected_value
    assert schemas == original_schemas
