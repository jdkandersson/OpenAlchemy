"""Tests for converting simple types."""

import datetime

import pytest

from open_alchemy import utility_base


@pytest.mark.parametrize(
    "format_, value, expected_value",
    [
        (None, 1, 1),
        ("int32", 1, 1),
        ("int64", 1, 1),
        (None, 1.1, 1.1),
        ("float", 1.1, 1.1),
        (None, "value 1", "value 1"),
        ("password", "value 1", "value 1"),
        ("byte", "value 1", "value 1"),
        ("binary", b"value 1", "value 1"),
        ("date", datetime.date(2000, 1, 1), "2000-01-01"),
        ("date", datetime.datetime(2000, 1, 1, 1, 1, 1), "2000-01-01T01:01:01"),
        (None, True, True),
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
def test_convert(format_, value, expected_value):
    """
    GIVEN format, value and expected value
    WHEN convert is called with the value and format
    THEN the expected value is returned.
    """
    returned_value = utility_base.to_dict.simple.convert(format_=format_, value=value)

    assert returned_value == expected_value
