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


@pytest.mark.helper
def test_type():
    """
    GIVEN schema with type
    WHEN type_ is called with the schema
    THEN the type of the schema is returned.
    """
    type_ = "type 1"
    schema = {"type": type_}

    returned_type = helpers.peek.type_(schema=schema, schemas={})

    assert returned_type == type_


@pytest.mark.parametrize(
    "schema", [{"nullable": "1"}, {"nullable": 1}, {"nullable": 1.1}],
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


@pytest.mark.parametrize(
    "schema, expected_nullable",
    [({}, None), ({"nullable": True}, True), ({"nullable": False}, False)],
    ids=["missing", "true", "false"],
)
@pytest.mark.helper
def test_nullable(schema, expected_nullable):
    """
    GIVEN schema and expected nullable
    WHEN nullable is called with the schema
    THEN the expected nullable is returned.
    """
    returned_nullable = helpers.peek.nullable(schema=schema, schemas={})

    assert returned_nullable == expected_nullable


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
    "schema, expected_format",
    [({}, None), ({"format": "format 1"}, "format 1")],
    ids=["missing", "present"],
)
@pytest.mark.helper
def test_format(schema, expected_format):
    """
    GIVEN schema and expected format
    WHEN format_ is called with the schema
    THEN the expected format is returned.
    """
    returned_format = helpers.peek.format_(schema=schema, schemas={})

    assert returned_format == expected_format


@pytest.mark.parametrize(
    "schema", [{"maxLength": "1"}, {"maxLength": True}],
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


@pytest.mark.parametrize(
    "schema, expected_max_length",
    [({}, None), ({"maxLength": 1}, 1)],
    ids=["missing", "present"],
)
@pytest.mark.helper
def test_max_length(schema, expected_max_length):
    """
    GIVEN schema and expected max_length
    WHEN max_length is called with the schema
    THEN the expected max_length is returned.
    """
    returned_max_length = helpers.peek.max_length(schema=schema, schemas={})

    assert returned_max_length == expected_max_length


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


@pytest.mark.parametrize(
    "schema, expected_read_only",
    [({}, None), ({"readOnly": False}, False), ({"readOnly": True}, True)],
    ids=["missing", "false", "true"],
)
@pytest.mark.helper
def test_read_only(schema, expected_read_only):
    """
    GIVEN schema and expected readOnly
    WHEN read_only is called with the schema
    THEN the expected readOnly is returned.
    """

    returned_read_only = helpers.peek.read_only(schema=schema, schemas={})

    assert returned_read_only == expected_read_only


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


@pytest.mark.parametrize(
    "schema, expected_write_only",
    [({}, None), ({"writeOnly": False}, False), ({"writeOnly": True}, True)],
    ids=["missing", "false", "true"],
)
@pytest.mark.helper
def test_write_only(schema, expected_write_only):
    """
    GIVEN schema and expected writeOnly
    WHEN write_only is called with the schema
    THEN the expected writeOnly is returned.
    """

    returned_write_only = helpers.peek.write_only(schema=schema, schemas={})

    assert returned_write_only == expected_write_only


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


@pytest.mark.parametrize(
    "schema, expected_description",
    [({}, None), ({"description": "description 1"}, "description 1")],
    ids=["missing", "present"],
)
@pytest.mark.helper
def test_description(schema, expected_description):
    """
    GIVEN schema and expected description
    WHEN description is called with the schema
    THEN the expected description is returned.
    """
    returned_description = helpers.peek.description(schema=schema, schemas={})

    assert returned_description == expected_description


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


@pytest.mark.parametrize(
    "schema, expected_items",
    [({}, None), ({"items": {"key": "value"}}, {"key": "value"})],
    ids=["missing", "defined"],
)
@pytest.mark.helper
def test_items(schema, expected_items):
    """
    GIVEN schema and expected items
    WHEN items is called with the schema
    THEN the expected items is returned.
    """
    returned_items = helpers.peek.items(schema=schema, schemas={})

    assert returned_items == expected_items


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
    "schema, expected_ref",
    [
        ({}, None),
        ({"$ref": "value"}, "value"),
        ({"allOf": [{"$ref": "value"}]}, "value"),
    ],
    ids=["missing", "defined", "allOf"],
)
@pytest.mark.helper
def test_ref(schema, expected_ref):
    """
    GIVEN schema and expected $ref
    WHEN $ref is called with the schema
    THEN the expected $ref is returned.
    """
    returned_ref = helpers.peek.ref(schema=schema, schemas={})

    assert returned_ref == expected_ref


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
