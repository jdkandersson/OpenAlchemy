"""Tests for retrieving artifacts of a backref property."""

import copy
import functools
import typing

import pytest

from open_alchemy.schemas import artifacts
from open_alchemy.schemas.helpers.property_ import type_

DEFAULT_SCHEMA: typing.Any = {"type": "object"}
GET_TESTS = [
    pytest.param(
        {**DEFAULT_SCHEMA}, {}, "type_", type_.Type.BACKREF, id="property type"
    ),
    pytest.param(
        {**DEFAULT_SCHEMA, "type": "object"},
        {},
        "sub_type",
        artifacts.types.BackrefSubType.OBJECT,
        id="sub type",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {**DEFAULT_SCHEMA, "type": "array"}},
        "sub_type",
        artifacts.types.BackrefSubType.ARRAY,
        id="$ref sub type",
    ),
    pytest.param(
        {"allOf": [{**DEFAULT_SCHEMA, "type": "object"}]},
        {},
        "sub_type",
        artifacts.types.BackrefSubType.OBJECT,
        id="allOf sub type",
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
