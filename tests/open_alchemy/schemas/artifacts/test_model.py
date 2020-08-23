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
    pytest.param({**DEFAULT_SCHEMA}, {}, "inherits", None, id="inherits not defined",),
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
        {**DEFAULT_SCHEMA}, {}, "description", None, id="description not defined",
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
        {"allOf": [{**DEFAULT_SCHEMA, "description": "description 3",}]},
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
    returned_artifacts = artifacts.model.get(schema=schema, schemas=schemas)

    assert getattr(returned_artifacts, key) == expected_value
