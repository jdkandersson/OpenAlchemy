"""Tests for peek helpers."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas",
    [({}, {}), ({"type": True}, {})],
    ids=["plain", "not string value"],
)
@pytest.mark.helper
def test_type_no_type(schema, schemas):
    """
    GIVEN schema without a type
    WHEN type_ is called with the schema
    THEN TypeMissingError is raised.
    """
    with pytest.raises(exceptions.TypeMissingError):
        helpers.peek.type_(schema=schema, schemas=schemas)


VALID_TESTS = [
    pytest.param([("type", "type 1")], helpers.peek.type_, "type 1", id="type"),
    pytest.param([], helpers.peek.nullable, None, id="nullable missing"),
    pytest.param(
        [("nullable", True)], helpers.peek.nullable, True, id="nullable defined"
    ),
    pytest.param(
        [("nullable", False)],
        helpers.peek.nullable,
        False,
        id="nullable defined different",
    ),
    pytest.param([], helpers.peek.format_, None, id="format missing"),
    pytest.param(
        [("format", "format 1")],
        helpers.peek.format_,
        "format 1",
        id="format defined",
    ),
    pytest.param(
        [("format", "format 2")],
        helpers.peek.format_,
        "format 2",
        id="format defined different",
    ),
    pytest.param([], helpers.peek.max_length, None, id="maxLength missing"),
    pytest.param(
        [("maxLength", 1)], helpers.peek.max_length, 1, id="maxLength defined"
    ),
    pytest.param(
        [("maxLength", 2)],
        helpers.peek.max_length,
        2,
        id="maxLength defined different",
    ),
    pytest.param([], helpers.peek.read_only, None, id="readOnly missing"),
    pytest.param(
        [("readOnly", True)], helpers.peek.read_only, True, id="readOnly defined"
    ),
    pytest.param(
        [("readOnly", False)],
        helpers.peek.read_only,
        False,
        id="readOnly defined different",
    ),
    pytest.param([], helpers.peek.write_only, None, id="writeOnly missing"),
    pytest.param(
        [("writeOnly", True)], helpers.peek.write_only, True, id="writeOnly defined"
    ),
    pytest.param(
        [("writeOnly", False)],
        helpers.peek.write_only,
        False,
        id="writeOnly defined different",
    ),
    pytest.param([], helpers.peek.description, None, id="description missing"),
    pytest.param(
        [("description", "description 1")],
        helpers.peek.description,
        "description 1",
        id="description defined",
    ),
    pytest.param(
        [("description", "description 2")],
        helpers.peek.description,
        "description 2",
        id="description defined different",
    ),
    pytest.param([], helpers.peek.items, None, id="items missing"),
    pytest.param(
        [("items", {"key_1": "value 1"})],
        helpers.peek.items,
        {"key_1": "value 1"},
        id="items defined",
    ),
    pytest.param(
        [("items", {"key_2": "value 2"})],
        helpers.peek.items,
        {"key_2": "value 2"},
        id="items defined different",
    ),
    pytest.param([], helpers.peek.ref, None, id="ref missing"),
    pytest.param(
        [("$ref", "value 1")],
        helpers.peek.ref,
        "value 1",
        id="ref defined",
    ),
    pytest.param(
        [("allOf", [{"$ref": "value 2"}])],
        helpers.peek.ref,
        "value 2",
        id="ref defined different",
    ),
]


@pytest.mark.parametrize("key_values, func, expected_value", VALID_TESTS)
@pytest.mark.helper
def test_type(key_values, func, expected_value):
    """
    GIVEN key and values for a schema and a function
    WHEN the function is called with the schema
    THEN expected value is returned.
    """
    schema = dict(key_values)

    returned_type = func(schema=schema, schemas={})

    assert returned_type == expected_value


@pytest.mark.parametrize(
    "schema",
    [{"nullable": "1"}, {"nullable": 1}, {"nullable": 1.1}],
)
@pytest.mark.helper
def test_nullable_wrong_type(schema):
    """
    GIVEN schema with nullable defined as a string
    WHEN nullable is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.nullable(schema=schema, schemas={})


@pytest.mark.helper
def test_format_wrong_type():
    """
    GIVEN schema with format defined as a boolean
    WHEN format_ is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"format": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.format_(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema",
    [{"maxLength": "1"}, {"maxLength": True}],
)
@pytest.mark.helper
def test_max_length_wrong_type(schema):
    """
    GIVEN schema with max_length of the wrong type
    WHEN max_length is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.max_length(schema=schema, schemas={})


@pytest.mark.helper
def test_read_only_wrong_type():
    """
    GIVEN schema with readOnly defined as a string
    WHEN read_only is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"readOnly": "true"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.read_only(schema=schema, schemas={})


@pytest.mark.helper
def test_write_only_wrong_type():
    """
    GIVEN schema with writeOnly defined as a string
    WHEN write_only is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"writeOnly": "true"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.write_only(schema=schema, schemas={})


@pytest.mark.helper
def test_description_wrong_type():
    """
    GIVEN schema with description defined as a boolean
    WHEN description is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"description": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.description(schema=schema, schemas={})


@pytest.mark.helper
def test_items_wrong_type():
    """
    GIVEN schema with items defined as a boolean
    WHEN items is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"items": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.items(schema=schema, schemas={})


@pytest.mark.helper
def test_ref_wrong_type():
    """
    GIVEN schema with $ref defined as a boolean
    WHEN $ref is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"$ref": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.ref(schema=schema, schemas={})


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
        helpers.peek.default(schema=schema, schemas={})


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
    default = helpers.peek.default(schema=schema, schemas=schemas)

    assert default == expected_default
