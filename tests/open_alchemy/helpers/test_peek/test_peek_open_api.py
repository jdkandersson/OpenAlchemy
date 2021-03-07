"""Tests for peek helpers."""

import pytest

from open_alchemy import exceptions
from open_alchemy.helpers import peek


@pytest.mark.parametrize(
    "schema",
    [
        {},
        {"type": True},
        {"type": ["type 1", "type 2"]},
        {"type": ["type 1", "type 2", "null"]},
    ],
    ids=[
        "plain",
        "not string value",
        "multiple types not null",
        "multiples types with null",
    ],
)
@pytest.mark.helper
def test_type_invalid(schema):
    """
    GIVEN schema with an invalid type
    WHEN type_ is called with the schema
    THEN TypeMissingError is raised.
    """
    with pytest.raises(exceptions.TypeMissingError):
        peek.type_(schema=schema, schemas={})


VALID_TESTS = [
    pytest.param([("type", "type 1")], peek.type_, "type 1", id="type"),
    pytest.param([("type", ["type 1"])], peek.type_, "type 1", id="type openapi 3.1"),
    pytest.param(
        [("type", ["type 1", "null"])],
        peek.type_,
        "type 1",
        id="type openapi 3.1 with null last",
    ),
    pytest.param(
        [("type", ["null", "type 1"])],
        peek.type_,
        "type 1",
        id="type openapi 3.1 with null first",
    ),
    pytest.param([], peek.nullable, None, id="nullable missing"),
    pytest.param([("nullable", True)], peek.nullable, True, id="nullable defined"),
    pytest.param(
        [("nullable", False)],
        peek.nullable,
        False,
        id="nullable defined different",
    ),
    pytest.param(
        [("type", [])],
        peek.nullable,
        False,
        id="nullable openapi 3.1 not null",
    ),
    pytest.param(
        [("type", ["null"])],
        peek.nullable,
        True,
        id="nullable openapi 3.1 null",
    ),
    pytest.param(
        [("type", ["type 1", "null"])],
        peek.nullable,
        True,
        id="nullable openapi 3.1 null with type first",
    ),
    pytest.param(
        [("type", ["null", "type 1"])],
        peek.nullable,
        True,
        id="nullable openapi 3.1 null with type last",
    ),
    pytest.param(
        [("type", []), ("nullable", False)],
        peek.nullable,
        False,
        id="nullable openapi 3.1 false and 3.0 false",
    ),
    pytest.param(
        [("type", ["null"]), ("nullable", False)],
        peek.nullable,
        True,
        id="nullable openapi 3.1 true and 3.0 false",
    ),
    pytest.param(
        [("type", []), ("nullable", True)],
        peek.nullable,
        True,
        id="nullable openapi 3.1 false and 3.0 true",
    ),
    pytest.param(
        [("type", ["null"]), ("nullable", True)],
        peek.nullable,
        True,
        id="nullable openapi 3.1 true and 3.0 true",
    ),
    pytest.param([], peek.format_, None, id="format missing"),
    pytest.param(
        [("format", "format 1")],
        peek.format_,
        "format 1",
        id="format defined",
    ),
    pytest.param(
        [("format", "format 2")],
        peek.format_,
        "format 2",
        id="format defined different",
    ),
    pytest.param([], peek.max_length, None, id="maxLength missing"),
    pytest.param([("maxLength", 1)], peek.max_length, 1, id="maxLength defined"),
    pytest.param(
        [("maxLength", 2)],
        peek.max_length,
        2,
        id="maxLength defined different",
    ),
    pytest.param([], peek.read_only, None, id="readOnly missing"),
    pytest.param([("readOnly", True)], peek.read_only, True, id="readOnly defined"),
    pytest.param(
        [("readOnly", False)],
        peek.read_only,
        False,
        id="readOnly defined different",
    ),
    pytest.param([], peek.write_only, None, id="writeOnly missing"),
    pytest.param([("writeOnly", True)], peek.write_only, True, id="writeOnly defined"),
    pytest.param(
        [("writeOnly", False)],
        peek.write_only,
        False,
        id="writeOnly defined different",
    ),
    pytest.param([], peek.description, None, id="description missing"),
    pytest.param(
        [("description", "description 1")],
        peek.description,
        "description 1",
        id="description defined",
    ),
    pytest.param(
        [("description", "description 2")],
        peek.description,
        "description 2",
        id="description defined different",
    ),
    pytest.param([], peek.items, None, id="items missing"),
    pytest.param(
        [("items", {"key_1": "value 1"})],
        peek.items,
        {"key_1": "value 1"},
        id="items defined",
    ),
    pytest.param(
        [("items", {"key_2": "value 2"})],
        peek.items,
        {"key_2": "value 2"},
        id="items defined different",
    ),
    pytest.param([], peek.ref, None, id="ref missing"),
    pytest.param(
        [("$ref", "value 1")],
        peek.ref,
        "value 1",
        id="ref defined",
    ),
    pytest.param(
        [("allOf", [{"$ref": "value 2"}])],
        peek.ref,
        "value 2",
        id="ref defined different",
    ),
]


@pytest.mark.parametrize("key_values, func, expected_value", VALID_TESTS)
@pytest.mark.helper
def test_key_value(key_values, func, expected_value):
    """
    GIVEN key and values for a schema and a function
    WHEN the function is called with the schema
    THEN expected value is returned.
    """
    schema = dict(key_values)

    returned_type = func(schema=schema, schemas={})

    assert returned_type == expected_value


INVALID_TESTS = [
    pytest.param("nullable", "1", peek.nullable, "boolean", id="nullable string"),
    pytest.param("nullable", 1, peek.nullable, "boolean", id="nullable integer"),
    pytest.param("nullable", 1.1, peek.nullable, "boolean", id="nullable number"),
    pytest.param("format", True, peek.format_, "string", id="format"),
    pytest.param("maxLength", "1", peek.max_length, "integer", id="maxLength"),
    pytest.param("readOnly", "1", peek.read_only, "boolean", id="readOnly"),
    pytest.param("writeOnly", "1", peek.write_only, "boolean", id="writeOnly"),
    pytest.param("description", True, peek.description, "string", id="description"),
    pytest.param("items", True, peek.items, "dict", id="items"),
    pytest.param("$ref", True, peek.ref, "string", id="$ref"),
]


@pytest.mark.parametrize("key, value, func, expected_type", INVALID_TESTS)
@pytest.mark.helper
def test_key_value_wrong_type(key, value, func, expected_type):
    """
    GIVEN key and value for a schema and function
    WHEN the function is called with the schema
    THEN MalformedSchemaError is raised where the message contains the key and expected
        type.
    """
    schema = {key: value}

    with pytest.raises(exceptions.MalformedSchemaError) as exc:
        func(schema=schema, schemas={})

    assert key in str(exc)
    assert expected_type in str(exc)


@pytest.mark.parametrize(
    "schema",
    [
        {"type": "integer", "default": "1"},
        {"type": "string", "maxLength": 1, "default": "value 1"},
    ],
    ids=["default different to schema type", "default different to schema maxLength"],
)
@pytest.mark.helper
def test_default_invalid(schema):
    """
    GIVEN schema with an invalid default
    WHEN default is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        peek.default(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, schemas, expected_default",
    [
        ({"type": "integer"}, {}, None),
        ({"type": "integer", "default": 1}, {}, 1),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "integer", "default": 1}},
            1,
        ),
        ({"type": "integer", "format": "int32", "default": 1}, {}, 1),
    ],
    ids=["no default", "default given", "$ref with default", "format with default"],
)
@pytest.mark.helper
def test_default(schema, schemas, expected_default):
    """
    GIVEN schema
    WHEN default is called with the schema
    THEN the expected default value is returned.
    """
    default = peek.default(schema=schema, schemas=schemas)

    assert default == expected_default
