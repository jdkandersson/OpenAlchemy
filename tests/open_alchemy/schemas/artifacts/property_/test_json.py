"""Tests for retrieving artifacts of a simple property."""

import functools

import pytest

from open_alchemy.schemas import artifacts
from open_alchemy.schemas.helpers.property_ import type_

GET_TESTS = [
    pytest.param({}, {}, "type_", type_.Type.JSON, id="property type"),
    pytest.param({}, {}, "open_api.nullable", None, id="nullable undefined"),
    pytest.param({"nullable": True}, {}, "open_api.nullable", True, id="nullable",),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"nullable": False}},
        "open_api.nullable",
        False,
        id="$ref nullable",
    ),
    pytest.param(
        {"allOf": [{"nullable": None}]},
        {},
        "open_api.nullable",
        None,
        id="allOf nullable",
    ),
    pytest.param({}, {}, "open_api.description", None, id="description undefined"),
    pytest.param(
        {"description": "description 1"},
        {},
        "open_api.description",
        "description 1",
        id="description",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"description": "description  2"}},
        "open_api.description",
        "description  2",
        id="$ref description",
    ),
    pytest.param(
        {"allOf": [{"description": "description 3"}]},
        {},
        "open_api.description",
        "description 3",
        id="allOf description",
    ),
    pytest.param({}, {}, "open_api.read_only", None, id="readOnly undefined"),
    pytest.param({"readOnly": True}, {}, "open_api.read_only", True, id="readOnly",),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"readOnly": False}},
        "open_api.read_only",
        False,
        id="$ref readOnly",
    ),
    pytest.param(
        {"allOf": [{"readOnly": None}]},
        {},
        "open_api.read_only",
        None,
        id="allOf readOnly",
    ),
    pytest.param({}, {}, "open_api.write_only", None, id="writeOnly undefined"),
    pytest.param({"writeOnly": True}, {}, "open_api.write_only", True, id="writeOnly",),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"writeOnly": False}},
        "open_api.write_only",
        False,
        id="$ref writeOnly",
    ),
    pytest.param(
        {"allOf": [{"writeOnly": None}]},
        {},
        "open_api.write_only",
        None,
        id="allOf writeOnly",
    ),
    pytest.param({}, {}, "extension.primary_key", False, id="x-primary-key undefined",),
    pytest.param(
        {"x-primary-key": True}, {}, "extension.primary_key", True, id="x-primary-key",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-primary-key": False}},
        "extension.primary_key",
        False,
        id="$ref x-primary-key",
    ),
    pytest.param(
        {"allOf": [{"x-primary-key": None}]},
        {},
        "extension.primary_key",
        False,
        id="allOf x-primary-key",
    ),
    pytest.param({}, {}, "extension.index", None, id="x-index undefined"),
    pytest.param({"x-index": True}, {}, "extension.index", True, id="x-index",),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-index": False}},
        "extension.index",
        False,
        id="$ref x-index",
    ),
    pytest.param(
        {"allOf": [{"x-index": None}]}, {}, "extension.index", None, id="allOf x-index",
    ),
    pytest.param({}, {}, "extension.unique", None, id="x-unique undefined"),
    pytest.param({"x-unique": True}, {}, "extension.unique", True, id="x-unique",),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-unique": False}},
        "extension.unique",
        False,
        id="$ref x-unique",
    ),
    pytest.param(
        {"allOf": [{"x-unique": None}]},
        {},
        "extension.unique",
        None,
        id="allOf x-unique",
    ),
    pytest.param({}, {}, "extension.foreign_key", None, id="x-foreign-key undefined",),
    pytest.param(
        {"x-foreign-key": "foreign.key1"},
        {},
        "extension.foreign_key",
        "foreign.key1",
        id="x-foreign-key",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-foreign-key": "foreign.key2"}},
        "extension.foreign_key",
        "foreign.key2",
        id="$ref x-foreign-key",
    ),
    pytest.param(
        {"allOf": [{"x-foreign-key": "foreign.key3"}]},
        {},
        "extension.foreign_key",
        "foreign.key3",
        id="allOf x-foreign-key",
    ),
    pytest.param({}, {}, "extension.kwargs", None, id="x-kwargs undefined",),
    pytest.param(
        {"x-kwargs": {"key_1": "value 1"}},
        {},
        "extension.kwargs",
        {"key_1": "value 1"},
        id="x-kwargs",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-kwargs": {"key_2": "value 2"}}},
        "extension.kwargs",
        {"key_2": "value 2"},
        id="$ref x-kwargs",
    ),
    pytest.param(
        {"allOf": [{"x-kwargs": {"key_3": "value 3"}}]},
        {},
        "extension.kwargs",
        {"key_3": "value 3"},
        id="allOf x-kwargs",
    ),
    pytest.param(
        {}, {}, "extension.foreign_key_kwargs", None, id="x-kwargs undefined",
    ),
    pytest.param(
        {"x-foreign-key-kwargs": {"key_1": "value 1"}},
        {},
        "extension.foreign_key_kwargs",
        {"key_1": "value 1"},
        id="x-foreign-key-kwargs",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-foreign-key-kwargs": {"key_2": "value 2"}}},
        "extension.foreign_key_kwargs",
        {"key_2": "value 2"},
        id="$ref x-foreign-key-kwargs",
    ),
    pytest.param(
        {"allOf": [{"x-foreign-key-kwargs": {"key_3": "value 3"}}]},
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
    returned_artifacts = artifacts.property_.json.get(schemas, schema)

    value = functools.reduce(getattr, key.split("."), returned_artifacts)
    assert value == expected_value
