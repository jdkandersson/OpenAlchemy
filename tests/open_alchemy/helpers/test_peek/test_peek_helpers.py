"""Tests for peek helpers."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas, expected_value",
    [
        ({}, {}, None),
        ({"key": "value 1"}, {}, "value 1"),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"key": "value 1"}},
            "value 1",
        ),
        ({"allOf": []}, {}, None),
        ({"allOf": [{"key": "value 1"}]}, {}, "value 1"),
        ({"allOf": [{}]}, {}, None),
        ({"allOf": [{"key": "value 1"}, {"key": "value 2"}]}, {}, "value 1"),
        ({"allOf": [{"key": "value 2"}, {"key": "value 1"}]}, {}, "value 2"),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"key": "value 1"}]}},
            "value 1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"key": "value 1"}]}},
            "value 1",
        ),
    ],
    ids=[
        "missing",
        "plain",
        "$ref",
        "allOf empty",
        "allOf single no type",
        "allOf single",
        "allOf multiple first",
        "allOf multiple last",
        "$ref then allOf",
        "allOf with $ref",
    ],
)
@pytest.mark.helper
def test_peek_key(schema, schemas, expected_value):
    """
    GIVEN schema, schemas and expected value
    WHEN peek_key is called with the schema and schemas
    THEN the expected value is returned.
    """
    returned_type = helpers.peek.peek_key(schema=schema, schemas=schemas, key="key")

    assert returned_type == expected_value


@pytest.mark.parametrize(
    "schema, schemas",
    [
        pytest.param(True, {}, id="schema not dictionary"),
        pytest.param({}, True, id="schemas not dictionary"),
        pytest.param({"$ref": True}, {}, id="$ref not string"),
        pytest.param({"allOf": True}, {}, id="allOf list"),
        pytest.param({"allOf": [True]}, {}, id="allOf element not dict"),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"$ref": "#/components/schemas/RefSchema"}},
            id="single step circular $ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {"$ref": "#/components/schemas/NestedRefSchema"},
                "NestedRefSchema": {"$ref": "#/components/schemas/RefSchema"},
            },
            id="multiple step circular $ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}},
            id="allOf single step circular $ref",
        ),
    ],
)
@pytest.mark.helper
def test_peek_key_invalid(schema, schemas):
    """
    GIVEN schema, schemas that are invalid
    WHEN peek_key is called with the schema and schemas
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.peek_key(schema=schema, schemas=schemas, key="key")


@pytest.mark.parametrize(
    "schema, schemas, expected_value",
    [
        pytest.param({}, {}, None, id="not found",),
        pytest.param({"x-backref": "schema"}, {}, "schema", id="present locally",),
        pytest.param({"allOf": []}, {}, None, id="not present locally in allOf",),
        pytest.param(
            {"allOf": [{"x-backref": "schema"}]},
            {},
            "schema",
            id="present locally in allOf",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            None,
            id="not present behind $ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-backref": "schema"}},
            "schema",
            id="present behind $ref",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-backref": "schema"},
                    {"$ref": "#/components/schemas/RefSchema"},
                ]
            },
            {"RefSchema": {"x-backref": "wrong_schema"}},
            "schema",
            id="present locally in allOf and behind $ref",
        ),
    ],
)
@pytest.mark.helper
def test_get(schema, schemas, expected_value):
    """
    GIVEN schema, schemas and expected value
    WHEN get is called with the backref peek helper and the schema and schemas
    THEN the expected value is returned.
    """
    returned_value = helpers.peek.prefer_local(
        get_value=helpers.peek.backref, schema=schema, schemas=schemas
    )

    assert returned_value == expected_value
