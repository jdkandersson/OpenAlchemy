"""Tests for retrieving artifacts of a backref property."""

import copy
import functools
import typing

import pytest

from open_alchemy.schemas import artifacts
from open_alchemy.schemas.helpers.property_ import type_

DEFAULT_SCHEMA: typing.Any = {"type": "object"}
GET_TESTS = [
    pytest.param({**DEFAULT_SCHEMA}, {}, "required", None, id="required"),
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "type", type_.Type.BACKREF, id="property type"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "type": "object"},
        {},
        "sub_type",
        artifacts.types.BackrefSubType.OBJECT,
        id="sub type object",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "type": "array", "items": {}}},
        "sub_type",
        artifacts.types.BackrefSubType.ARRAY,
        id="$ref sub type array",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "type": "object"}]},
        {},
        "sub_type",
        artifacts.types.BackrefSubType.OBJECT,
        id="allOf sub type object",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "type": "object"},
        {},
        "properties",
        [],
        id="properties object no properties",
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "type": "object", "properties": {}},
        {},
        "properties",
        [],
        id="properties object empty",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "type": "object",
            "properties": {"prop_1": {"key_1": "value 1"}},
        },
        {},
        "properties",
        ["prop_1"],
        id="properties object single",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "type": "object",
            "properties": {
                "prop_1": {"key_1": "value 1"},
                "prop_2": {"key_2": "value 2"},
            },
        },
        {},
        "properties",
        ["prop_1", "prop_2"],
        id="properties object multiple",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "type": "array",
            "items": {"properties": {"prop_1": {"key_1": "value 1"}}},
        },
        {},
        "properties",
        ["prop_1"],
        id="properties array single",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                **DEFAULT_SCHEMA,
                "type": "array",
                "items": {"properties": {"prop_1": {"key_1": "value 1"}}},
            }
        },
        "properties",
        ["prop_1"],
        id="$ref properties array single",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    **DEFAULT_SCHEMA,
                    "type": "array",
                    "items": {"properties": {"prop_1": {"key_1": "value 1"}}},
                }
            ]
        },
        {},
        "properties",
        ["prop_1"],
        id="allOf properties array single",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "type": "object",
            "properties": {"prop_1": {"key_1": "value 1"}},
        },
        {},
        "schema",
        {
            **DEFAULT_SCHEMA,
            "type": "object",
            "properties": {"prop_1": {"key_1": "value 1"}},
        },
        id="schema",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                **DEFAULT_SCHEMA,
                "type": "object",
                "properties": {"prop_1": {"key_1": "value 1"}},
            }
        },
        "schema",
        {
            **DEFAULT_SCHEMA,
            "type": "object",
            "properties": {"prop_1": {"key_1": "value 1"}},
        },
        id="$ref schema",
    ),
    pytest.param(
        {
            **DEFAULT_SCHEMA,
            "type": "object",
            "properties": {"prop_1": {"$ref": "#/components/schemas/RefSchema"}},
        },
        {"RefSchema": {"key_1": "value 1"}},
        "schema",
        {
            **DEFAULT_SCHEMA,
            "type": "object",
            "properties": {"prop_1": {"key_1": "value 1"}},
        },
        id="schema properties $ref",
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
        {"allOf": [{**DEFAULT_SCHEMA, "description": "description 3"}]},
        {},
        "description",
        "description 3",
        id="allOf description",
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

    returned_artifacts = artifacts.property_.backref.get(schemas, schema)

    value = functools.reduce(getattr, key.split("."), returned_artifacts)
    assert value == expected_value
    assert schemas == original_schemas
