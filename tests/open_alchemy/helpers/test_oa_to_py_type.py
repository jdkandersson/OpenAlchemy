"""Tests for oa_to_py_type."""

import datetime

import pytest

from open_alchemy import exceptions
from open_alchemy.helpers import oa_to_py_type


@pytest.mark.parametrize(
    "value, type_, format_",
    [
        (None, "object", None),
        (None, "array", None),
        (1.1, "number", "double"),
        ("value 1", "string", "date"),
        ("value 1", "string", "date-time"),
    ],
    ids=[
        "object",
        "array",
        "number double",
        "string date invalid",
        "string date-time invalid",
    ],
)
@pytest.mark.helper
def test_convert_invalid(value, type_, format_):
    """
    GIVEN value, type and format that is not valid
    WHEN value, type and format are passed to convert
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        oa_to_py_type.convert(value=value, type_=type_, format_=format_)


@pytest.mark.parametrize(
    "value, type_, format_, expected_value",
    [
        (None, "integer", None, None),
        (1, "integer", None, 1),
        (1, "integer", "int32", 1),
        (1, "integer", "int64", 1),
        (1.1, "number", None, 1.1),
        (1.1, "number", "float", 1.1),
        (True, "boolean", None, True),
        ("value 1", "string", None, "value 1"),
        ("value 1", "string", "password", "value 1"),
        ("value 1", "string", "byte", "value 1"),
        ("value 1", "string", "binary", b"value 1"),
        ("2000-01-01", "string", "date", datetime.date(year=2000, month=1, day=1)),
        (
            "2000-01-01T01:01:01",
            "string",
            "date-time",
            datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1),
        ),
    ],
    ids=[
        "None",
        "integer no format",
        "integer int32",
        "integer int64",
        "number no format",
        "number float",
        "boolean",
        "string no format",
        "string password",
        "string byte",
        "string binary",
        "string date",
        "string date-time",
    ],
)
@pytest.mark.helper
def test_convert(value, type_, format_, expected_value):
    """
    GIVEN value, type and format
    WHEN value, type and format are passed to convert
    THEN the expected value is returned.
    """
    returned_value = oa_to_py_type.convert(value=value, type_=type_, format_=format_)

    assert returned_value == expected_value
