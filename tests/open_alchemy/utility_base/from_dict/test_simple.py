"""Tests for converting simple types."""

import datetime
from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.parametrize(
    "schema, value, exception",
    [
        ({}, mock.MagicMock(), exceptions.TypeMissingError),
        ({"type": "type 1"}, mock.MagicMock(), exceptions.FeatureNotImplementedError),
        ({"type": "integer"}, 1.1, exceptions.InvalidInstanceError),
        ({"type": "number"}, 1, exceptions.InvalidInstanceError),
        ({"type": "string"}, 1, exceptions.InvalidInstanceError),
        ({"type": "boolean"}, 1, exceptions.InvalidInstanceError),
    ],
    ids=[
        "no type",
        "unsupported type",
        "integer different type",
        "number different type",
        "string different type",
        "boolean different type",
    ],
)
@pytest.mark.utility_base
def test_convert_invalid(schema, value, exception):
    """
    GIVEN invaid schema and expected exception
    WHEN convert is called with the schema
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        utility_base.from_dict.simple.convert(schema=schema, value=value)


@pytest.mark.parametrize(
    "schema, value, expected_value",
    [
        ({"type": "integer"}, 1, 1),
        ({"type": "integer", "format": "int32"}, 1, 1),
        ({"type": "integer", "format": "int64"}, 1, 1),
        ({"type": "number"}, 1.1, 1.1),
        ({"type": "number", "format": "float"}, 1.1, 1.1),
        ({"type": "string"}, "value 1", "value 1"),
        ({"type": "string", "format": "password"}, "value 1", "value 1"),
        ({"type": "string", "format": "byte"}, "value 1", "value 1"),
        ({"type": "string", "format": "binary"}, None, None),
        ({"type": "string", "format": "binary"}, "value 1", b"value 1"),
        ({"type": "string", "format": "date"}, None, None),
        ({"type": "string", "format": "date"}, "2000-01-01", datetime.date(2000, 1, 1)),
        ({"type": "string", "format": "date-time"}, None, None),
        (
            {"type": "string", "format": "date-time"},
            "2000-01-01T01:01:01",
            datetime.datetime(2000, 1, 1, 1, 1, 1),
        ),
        ({"type": "boolean"}, True, True),
    ],
    ids=[
        "integer",
        "integer int32",
        "integer int64",
        "number",
        "number  float",
        "string",
        "string  password",
        "string  byte",
        "string  binary None",
        "string  binary not NOne",
        "string  date None",
        "string  date not None",
        "string  date-time None",
        "string  date-time not None",
        "boolean",
    ],
)
@pytest.mark.utility_base
def test_convert(schema, value, expected_value):
    """
    GIVEN schema, value and expected value
    WHEN convert is called with the value and schema
    THEN the expected value is returned.
    """
    returned_value = utility_base.from_dict.simple.convert(schema=schema, value=value)

    assert returned_value == expected_value
