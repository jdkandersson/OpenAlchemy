"""Tests for converting arrays to a dictionary read value."""

from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.parametrize(
    "schema, value, exception",
    [
        ({}, mock.MagicMock(), exceptions.MalformedSchemaError),
        ({"items": {}}, mock.MagicMock(), exceptions.TypeMissingError),
        (
            {"items": {"type": "array"}},
            mock.MagicMock(),
            exceptions.FeatureNotImplementedError,
        ),
        (
            {"items": {"type": "string"}},
            mock.MagicMock(),
            exceptions.FeatureNotImplementedError,
        ),
        ({"items": {"type": "object"}}, 1, exceptions.InvalidInstanceError),
    ],
    ids=[
        "no item spec",
        "item spec no type",
        "item spec array type",
        "item spec not object type",
        "value not array",
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
        utility_base.to_dict.array.convert(schema=schema, value=value)


@pytest.mark.parametrize(
    "schema, value, expected_value",
    [
        ({"items": {"type": "object"}}, None, None),
        ({"items": {"type": "object"}}, [], []),
        (
            {"items": {"type": "object"}},
            [mock.MagicMock(to_dict=lambda: {"key": "value"})],
            [{"key": "value"}],
        ),
        (
            {
                "items": {"type": "object", "properties": {"key": "type 1"}},
                "readOnly": True,
            },
            [mock.MagicMock(key="value")],
            [{"key": "value"}],
        ),
        (
            {"items": {"type": "object"}},
            [
                mock.MagicMock(to_dict=lambda: {"key": "value 1"}),
                mock.MagicMock(to_dict=lambda: {"key": "value 2"}),
            ],
            [{"key": "value 1"}, {"key": "value 2"}],
        ),
    ],
    ids=["None", "empty", "single relationship", "single readOnly", "multiple"],
)
@pytest.mark.utility_base
def test_convert_valid(value, schema, expected_value):
    """
    GIVEN valid schema and value and expected value
    WHEN convert is called with the schema and value
    THEN the expected value is returned.
    """
    returned_value = utility_base.to_dict.array.convert(schema=schema, value=value)

    assert returned_value == expected_value
