"""Tests for to_dict."""

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
    ids=["missing type", "unsupported type"],
)
@pytest.mark.utility_base
def test_invalid(schema, exception):
    """
    GIVEN invalid schema and expected exception
    WHEN convert is called with the schema
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        utility_base.to_dict.convert(schema=schema, value=mock.MagicMock())


@pytest.mark.parametrize(
    "schema, value, expected_value",
    [
        ({"type": "string"}, "value", "value"),
        (
            {"type": "object", "properties": {"key": "type 1"}},
            mock.MagicMock(to_dict=lambda: {"key": "value"}),
            {"key": "value"},
        ),
        (
            {
                "type": "array",
                "items": {"type": "object", "properties": {"key": "type 1"}},
            },
            [mock.MagicMock(to_dict=lambda: {"key": "value"})],
            [{"key": "value"}],
        ),
    ],
    ids=["simple", "object", "array"],
)
@pytest.mark.utility_base
def test_valid(schema, value, expected_value):
    """
    GIVEN valid schema, value and expected value
    WHEN convert is called with the schema and value
    THEN the expected value is returned.
    """
    returned_value = utility_base.to_dict.convert(schema=schema, value=value)

    assert returned_value == expected_value
