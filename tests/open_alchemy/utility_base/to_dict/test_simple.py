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
        (
            {"type": "string", "format": "binary"},
            "value",
            exceptions.InvalidInstanceError,
        ),
        (
            {"type": "string", "format": "date"},
            "value",
            exceptions.InvalidInstanceError,
        ),
        (
            {"type": "string", "format": "date-time"},
            "value",
            exceptions.InvalidInstanceError,
        ),
        ({"type": "boolean"}, 1, exceptions.InvalidInstanceError),
    ],
    ids=[
        "no type",
        "unsupported type",
        "integer different type",
        "number different type",
        "string different type",
        "string binary different type",
        "string date different type",
        "string date-time different type",
        "boolean different type",
    ],
)
@pytest.mark.utility_base
def test_convert_invalid(schema, value, exception):
    """
    GIVEN invalid schema and expected exception
    WHEN convert is called with the schema
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        utility_base.to_dict.simple.convert(schema=schema, value=value)


@pytest.mark.parametrize(
    "schema, value, expected_value",
    [
        pytest.param(
            {"type": "integer"},
            1,
            1,
            id="integer",
        ),
        pytest.param(
            {"type": "integer", "format": "int32"},
            1,
            1,
            id="integer int32",
        ),
        pytest.param(
            {"type": "integer", "format": "int64"},
            1,
            1,
            id="integer int64",
        ),
        pytest.param(
            {"type": "number"},
            1.1,
            1.1,
            id="number",
        ),
        pytest.param(
            {"type": "number", "format": "float"},
            1.1,
            1.1,
            id="number  float",
        ),
        pytest.param(
            {"type": "string"},
            "value 1",
            "value 1",
            id="string",
        ),
        pytest.param(
            {"type": "string", "format": "password"},
            "value 1",
            "value 1",
            id="string  password",
        ),
        pytest.param(
            {"type": "string", "format": "unsupported"},
            "value 1",
            "value 1",
            id="string  unsupported",
        ),
        pytest.param(
            {"type": "string", "format": "byte"},
            "value 1",
            "value 1",
            id="string  byte",
        ),
        pytest.param(
            {"type": "string", "format": "binary"},
            None,
            None,
            id="string  binary None",
        ),
        pytest.param(
            {"type": "string", "format": "binary"},
            b"value 1",
            "value 1",
            id="string  binary not NOne",
        ),
        pytest.param(
            {"type": "string", "format": "date"},
            None,
            None,
            id="string  date None",
        ),
        pytest.param(
            {"type": "string", "format": "date"},
            datetime.date(2000, 1, 1),
            "2000-01-01",
            id="string  date not None",
        ),
        pytest.param(
            {"type": "string", "format": "date-time"},
            None,
            None,
            id="string  date-time None",
        ),
        pytest.param(
            {"type": "string", "format": "date-time"},
            datetime.datetime(2000, 1, 1, 1, 1, 1),
            "2000-01-01T01:01:01",
            id="string  date-time not None",
        ),
        pytest.param(
            {"type": "boolean"},
            True,
            True,
            id="boolean",
        ),
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
