"""Tests for retrieving artifacts of a simple property."""

import typing

import pytest

from open_alchemy.schemas import artifacts
from open_alchemy.schemas.helpers.property_ import type_

DEFAULT_SCHEMA: typing.Any = {"type": "default type"}
GET_TESTS = [
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "property_type", type_.Type.SIMPLE, id="property type"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "type": "type 1"}, {}, "type_", "type 1", id="type"
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "type": "type 1"}},
        "type_",
        "type 1",
        id="$ref type",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "type": "type 1"}]},
        {},
        "type_",
        "type 1",
        id="allOf type",
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

    assert getattr(returned_artifacts, key) == expected_value
