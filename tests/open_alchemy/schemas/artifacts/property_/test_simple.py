"""Tests for retrieving artifacts of a simple property."""

import copy
import functools
import typing

import pytest

from open_alchemy.schemas import artifacts
from open_alchemy.schemas.helpers.property_ import type_

DEFAULT_SCHEMA: typing.Any = {"type": "default type"}
GET_TESTS = [
    pytest.param(True, {**DEFAULT_SCHEMA}, {}, "required", True, id="required True"),
    pytest.param(False, {**DEFAULT_SCHEMA}, {}, "required", False, id="required False"),
    pytest.param(
        None, {**DEFAULT_SCHEMA}, {}, "type", type_.Type.SIMPLE, id="property type"
    ),
    pytest.param(
        None,
        {
            **DEFAULT_SCHEMA,
            "type": "string",
            "format": "format 1",
            "maxLength": 100,
            "description": "description 1",
            "nullable": True,
            "default": "default 1",
            "readOnly": False,
            "writeOnly": True,
        },
        {},
        "schema",
        {
            "type": "string",
            "format": "format 1",
            "maxLength": 100,
            "description": "description 1",
            "nullable": True,
            "default": "default 1",
            "readOnly": False,
            "writeOnly": True,
        },
        id="schema",
    ),
    pytest.param(
        None,
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
        None,
        {**DEFAULT_SCHEMA, "type": "type 1"},
        {},
        "open_api.type",
        "type 1",
        id="type",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "type": "type 2"}},
        "open_api.type",
        "type 2",
        id="$ref type",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "type": "type 4"},
            ]
        },
        {"RefSchema": {"type": "type 4"}},
        "open_api.type",
        "type 4",
        id="allOf type",
    ),
    pytest.param(
        None, {**DEFAULT_SCHEMA}, {}, "open_api.format", None, id="format undefined"
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "format": "format 1"},
        {},
        "open_api.format",
        "format 1",
        id="format",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "format": "format 2"}},
        "open_api.format",
        "format 2",
        id="$ref format",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "format": "format 3"},
            ]
        },
        {"RefSchema": {"format": "type 4"}},
        "open_api.format",
        "format 3",
        id="allOf format prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "open_api.max_length",
        None,
        id="maxLength undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "maxLength": 1},
        {},
        "open_api.max_length",
        1,
        id="maxLength",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "maxLength": 2}},
        "open_api.max_length",
        2,
        id="$ref maxLength",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "maxLength": 3},
            ]
        },
        {"RefSchema": {"maxLength": 4}},
        "open_api.max_length",
        3,
        id="allOf maxLength prefer local",
    ),
    pytest.param(
        None, {**DEFAULT_SCHEMA}, {}, "open_api.nullable", None, id="nullable undefined"
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "nullable": True},
        {},
        "open_api.nullable",
        True,
        id="nullable",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "nullable": False}},
        "open_api.nullable",
        False,
        id="$ref nullable",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "nullable": False},
            ]
        },
        {"RefSchema": {"nullable": True}},
        "open_api.nullable",
        False,
        id="allOf nullable prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "description",
        None,
        id="description undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "description": "description 1"},
        {},
        "description",
        "description 1",
        id="description",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "description": "description  2"}},
        "description",
        "description  2",
        id="$ref description",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "description": "description 3"},
            ]
        },
        {"RefSchema": {"description": "description 4"}},
        "description",
        "description 3",
        id="allOf description prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "type": "integer"},
        {},
        "open_api.default",
        None,
        id="default undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "type": "integer", "default": 1},
        {},
        "open_api.default",
        1,
        id="default",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "type": "integer", "default": 2}},
        "open_api.default",
        2,
        id="$ref default",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "type": "integer", "default": 3},
            ]
        },
        {"RefSchema": {"default": 4}},
        "open_api.default",
        3,
        id="allOf default prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "open_api.read_only",
        None,
        id="readOnly undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "readOnly": True},
        {},
        "open_api.read_only",
        True,
        id="readOnly",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "readOnly": False}},
        "open_api.read_only",
        False,
        id="$ref readOnly",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "readOnly": False},
            ]
        },
        {"RefSchema": {"readOnly": True}},
        "open_api.read_only",
        False,
        id="allOf readOnly prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "open_api.write_only",
        None,
        id="writeOnly undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "writeOnly": True},
        {},
        "open_api.write_only",
        True,
        id="writeOnly",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "writeOnly": False}},
        "open_api.write_only",
        False,
        id="$ref writeOnly",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "writeOnly": False},
            ]
        },
        {"RefSchema": {"writeOnly": True}},
        "open_api.write_only",
        False,
        id="allOf writeOnly prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "extension.primary_key",
        False,
        id="x-primary-key undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "x-primary-key": True},
        {},
        "extension.primary_key",
        True,
        id="x-primary-key",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-primary-key": False}},
        "extension.primary_key",
        False,
        id="$ref x-primary-key",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-primary-key": False},
            ]
        },
        {"RefSchema": {"x-primary-key": True}},
        "extension.primary_key",
        False,
        id="allOf x-primary-key prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "extension.autoincrement",
        None,
        id="x-autoincrement undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "x-autoincrement": True},
        {},
        "extension.autoincrement",
        True,
        id="x-autoincrement",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-autoincrement": False}},
        "extension.autoincrement",
        False,
        id="$ref x-autoincrement",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-autoincrement": False},
            ]
        },
        {"RefSchema": {"x-autoincrement": True}},
        "extension.autoincrement",
        False,
        id="allOf x-autoincrement prefer local",
    ),
    pytest.param(
        None, {**DEFAULT_SCHEMA}, {}, "extension.index", None, id="x-index undefined"
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "x-index": True},
        {},
        "extension.index",
        True,
        id="x-index",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-index": False}},
        "extension.index",
        False,
        id="$ref x-index",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-index": False},
            ]
        },
        {"RefSchema": {"x-index": True}},
        "extension.index",
        False,
        id="allOf x-index prefer local",
    ),
    pytest.param(
        None, {**DEFAULT_SCHEMA}, {}, "extension.unique", None, id="x-unique undefined"
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "x-unique": True},
        {},
        "extension.unique",
        True,
        id="x-unique",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-unique": False}},
        "extension.unique",
        False,
        id="$ref x-unique",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-unique": False},
            ]
        },
        {"RefSchema": {"x-unique": True}},
        "extension.unique",
        False,
        id="allOf x-unique prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "extension.foreign_key",
        None,
        id="x-foreign-key undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "x-foreign-key": "foreign.key1"},
        {},
        "extension.foreign_key",
        "foreign.key1",
        id="x-foreign-key",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-foreign-key": "foreign.key2"}},
        "extension.foreign_key",
        "foreign.key2",
        id="$ref x-foreign-key",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-foreign-key": "foreign.key3"},
            ]
        },
        {"RefSchema": {"x-foreign-key": "foreign.key4"}},
        "extension.foreign_key",
        "foreign.key3",
        id="allOf x-foreign-key prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "extension.kwargs",
        None,
        id="x-kwargs undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "x-kwargs": {"key_1": "value 1"}},
        {},
        "extension.kwargs",
        {"key_1": "value 1"},
        id="x-kwargs",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-kwargs": {"key_2": "value 2"}}},
        "extension.kwargs",
        {"key_2": "value 2"},
        id="$ref x-kwargs",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-kwargs": {"key_3": "value 3"}},
            ]
        },
        {"RefSchema": {"x-kwargs": {"key_4": "value 4"}}},
        "extension.kwargs",
        {"key_3": "value 3"},
        id="allOf x-kwargs prefer local",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "extension.foreign_key_kwargs",
        None,
        id="x-kwargs undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "x-foreign-key-kwargs": {"key_1": "value 1"}},
        {},
        "extension.foreign_key_kwargs",
        {"key_1": "value 1"},
        id="x-foreign-key-kwargs",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-foreign-key-kwargs": {"key_2": "value 2"}}},
        "extension.foreign_key_kwargs",
        {"key_2": "value 2"},
        id="$ref x-foreign-key-kwargs",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {**DEFAULT_SCHEMA, "x-foreign-key-kwargs": {"key_3": "value 3"}},
            ]
        },
        {"RefSchema": {"x-foreign-key-kwargs": {"key_4": "value 4"}}},
        "extension.foreign_key_kwargs",
        {"key_3": "value 3"},
        id="allOf x-foreign-key-kwargs",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA},
        {},
        "extension.dict_ignore",
        None,
        id="x-dict-ignore undefined",
    ),
    pytest.param(
        None,
        {**DEFAULT_SCHEMA, "x-dict-ignore": True},
        {},
        "extension.dict_ignore",
        True,
        id="x-dict-ignore",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "x-dict-ignore": False}},
        "extension.dict_ignore",
        False,
        id="$ref x-dict-ignore",
    ),
    pytest.param(
        None,
        {"allOf": [{**DEFAULT_SCHEMA, "x-dict-ignore": None}]},
        {},
        "extension.dict_ignore",
        None,
        id="allOf x-dict-ignore",
    ),
]


@pytest.mark.parametrize("required, schema, schemas, key, expected_value", GET_TESTS)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_get(required, schema, schemas, key, expected_value):
    """
    GIVEN schema, schemas, key and expected value
    WHEN get is called with the schema and schemas
    THEN the returned artifacts has the expected value behind the key.
    """
    original_schemas = copy.deepcopy(schemas)

    returned_artifacts = artifacts.property_.simple.get(schemas, schema, required)

    value = functools.reduce(getattr, key.split("."), returned_artifacts)
    assert value == expected_value
    assert schemas == original_schemas
