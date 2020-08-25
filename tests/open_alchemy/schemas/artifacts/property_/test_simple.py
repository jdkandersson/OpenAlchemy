"""Tests for retrieving artifacts of a simple property."""

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
        {**DEFAULT_SCHEMA}, {}, "extension.autoincrement", None, id="x-autoincrement"
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
        {**DEFAULT_SCHEMA}, {}, "extension.kwargs", None, id="x-kwargs not defined",
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
        {**DEFAULT_SCHEMA},
        {},
        "extension.foreign_key_kwargs",
        None,
        id="x-kwargs not defined",
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
    returned_artifacts = artifacts.property_.simple.get(schemas, schema)

    value = functools.reduce(getattr, key.split("."), returned_artifacts)
    assert value == expected_value
