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


@pytest.mark.helper
def test_read_only_wrong_type():
    """
    GIVEN schema without readOnly defined as a string
    WHEN read_only is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"readOnly": "true"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.read_only(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_read_only",
    [({}, False), ({"readOnly": False}, False), ({"readOnly": True}, True)],
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
    WHEN _peek_key is called with the schema and schemas
    THEN the expected value is returned.
    """
    # pylint: disable=protected-access
    returned_type = helpers.peek._peek_key(schema=schema, schemas=schemas, key="key")

    assert returned_type == expected_value
