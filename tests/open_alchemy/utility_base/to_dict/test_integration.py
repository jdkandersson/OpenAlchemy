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
        pytest.param({"type": "string"}, "value 1", "value 1", id="simple"),
        pytest.param({"type": "integer", "x-json": True}, 1, 1, id="json integer"),
        pytest.param({"type": "number", "x-json": True}, 1.1, 1.1, id="json number"),
        pytest.param(
            {"type": "string", "x-json": True}, "value 1", "value 1", id="json string"
        ),
        pytest.param(
            {"type": "boolean", "x-json": True}, True, True, id="json boolean"
        ),
        pytest.param(
            {"type": "object", "x-json": True},
            {"key": "value"},
            {"key": "value"},
            id="json object",
        ),
        pytest.param({"type": "array", "x-json": True}, [1], [1], id="json array"),
        pytest.param(
            {"type": "object", "properties": {"key": "type 1"}},
            mock.MagicMock(to_dict=lambda: {"key": "value"}),
            {"key": "value"},
            id="object",
        ),
        pytest.param(
            {
                "type": "array",
                "items": {"type": "object", "properties": {"key": "type 1"}},
            },
            [mock.MagicMock(to_dict=lambda: {"key": "value"})],
            [{"key": "value"}],
            id="array",
        ),
    ],
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
