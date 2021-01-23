"""Tests for peek helpers."""

import pytest

from open_alchemy import exceptions
from open_alchemy import types
from open_alchemy.helpers import peek


@pytest.mark.parametrize(
    "key, schema, schemas, expected_value",
    [
        pytest.param("key", {}, {}, None, id="missing"),
        pytest.param("key", {"key": "value 1"}, {}, "value 1", id="plain"),
        *(
            pytest.param(
                "x-key",
                {f"{prefix}key": "value 1"},
                {},
                "value 1",
                id=f"extension {prefix}",
            )
            for prefix in types.KeyPrefixes
        ),
        pytest.param(
            "key",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"key": "value 1"}},
            "value 1",
            id="$ref",
        ),
        pytest.param("key", {"allOf": []}, {}, None, id="allOf empty"),
        pytest.param(
            "key",
            {"allOf": [{"key": "value 1"}]},
            {},
            "value 1",
            id="allOf single no type",
        ),
        pytest.param("key", {"allOf": [{}]}, {}, None, id="allOf single"),
        pytest.param(
            "key",
            {"allOf": [{"key": "value 1"}, {"key": "value 2"}]},
            {},
            "value 1",
            id="allOf multiple first",
        ),
        pytest.param(
            "key",
            {"allOf": [{"key": "value 2"}, {"key": "value 1"}]},
            {},
            "value 2",
            id="allOf multiple last",
        ),
        pytest.param(
            "key",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"key": "value 1"}]}},
            "value 1",
            id="$ref then allOf",
        ),
        pytest.param(
            "key",
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"key": "value 1"}]}},
            "value 1",
            id="allOf with $ref",
        ),
    ],
)
@pytest.mark.helper
def test_peek_key(key, schema, schemas, expected_value):
    """
    GIVEN schema, schemas and expected value
    WHEN peek_key is called with the schema and schemas
    THEN the expected value is returned.
    """
    returned_type = peek.peek_key(schema=schema, schemas=schemas, key=key)

    assert returned_type == expected_value


@pytest.mark.parametrize(
    "schema, schemas, expected_value",
    [
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"key": "value 1"}},
            None,
            id="ref hit",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/OtherRefSchema"},
            {"OtherRefSchema": {"key": "value 1"}},
            "value 1",
            id="ref miss",
        ),
    ],
)
@pytest.mark.helper
def test_peek_key_skip_ref(schema, schemas, expected_value):
    """
    GIVEN schema, schemas and expected value
    WHEN peek_key is called with the schema and schemas
    THEN the expected value is returned.
    """
    returned_type = peek.peek_key(
        schema=schema, schemas=schemas, key="key", skip_ref="RefSchema"
    )

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
        peek.peek_key(schema=schema, schemas=schemas, key="key")


@pytest.mark.parametrize(
    "schema, schemas, expected_value",
    [
        pytest.param(
            {},
            {},
            None,
            id="not found",
        ),
        pytest.param(
            {"x-backref": "schema"},
            {},
            "schema",
            id="present locally",
        ),
        pytest.param(
            {"allOf": []},
            {},
            None,
            id="not present locally in allOf",
        ),
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
            id="present locally in allOf and behind $ref local first",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                ]
            },
            {"RefSchema": {"x-backref": "wrong_schema"}},
            "schema",
            id="present locally in allOf and behind $ref ref first",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "allOf": [
                        {"x-backref": "schema"},
                        {"$ref": "#/components/schemas/NestedRefSchema"},
                    ]
                },
                "NestedRefSchema": {"x-backref": "wrong_schema"},
            },
            "schema",
            id="$ref present locally in allOf and behind $ref local first",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "allOf": [
                        {"$ref": "#/components/schemas/NestedRefSchema"},
                        {"x-backref": "schema"},
                    ]
                },
                "NestedRefSchema": {"x-backref": "wrong_schema"},
            },
            "schema",
            id="$ref present locally in allOf and behind $ref ref first",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "allOf": [
                            {"$ref": "#/components/schemas/RefSchema"},
                            {"x-backref": "schema"},
                        ]
                    }
                ]
            },
            {
                "RefSchema": {"x-backref": "wrong_schema"},
            },
            "schema",
            id="$ref present locally in allOf and behind $ref ref first",
        ),
    ],
)
@pytest.mark.helper
def test_prefer_local(schema, schemas, expected_value):
    """
    GIVEN schema, schemas and expected value
    WHEN prefer_local is called with the backref peek helper and the schema and schemas
    THEN the expected value is returned.
    """
    returned_value = peek.prefer_local(
        get_value=peek.backref, schema=schema, schemas=schemas
    )

    assert returned_value == expected_value


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
def test_prefer_local_invalid(schema, schemas):
    """
    GIVEN schema, schemas that are invalid
    WHEN prefer_local is called with the schema and schemas
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        peek.prefer_local(get_value=peek.max_length, schema=schema, schemas=schemas)
