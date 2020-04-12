"""Tests for converting simple types."""

import datetime
from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.parametrize(
    "schema, exception",
    [
        ({}, exceptions.TypeMissingError),
        ({"type": "type 1"}, exceptions.FeatureNotImplementedError),
    ],
    ids=["no type", "unsupported type"],
)
@pytest.mark.utility_base
def test_convert_invalid(schema, exception):
    """
    GIVEN invaid schema and expected exception
    WHEN convert is called with the schema
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        utility_base.to_dict.simple.convert(schema=schema, value=mock.MagicMock())


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
        ({"type": "string", "format": "binary"}, b"value 1", "value 1"),
        ({"type": "string", "format": "date"}, datetime.date(2000, 1, 1), "2000-01-01"),
        (
            {"type": "string", "format": "date-time"},
            datetime.datetime(2000, 1, 1, 1, 1, 1),
            "2000-01-01T01:01:01",
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
        "string  binary",
        "string  date",
        "string  date-time",
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
    returned_value = utility_base.to_dict.simple.convert(schema=schema, value=value)

    assert returned_value == expected_value
