"""Tests for add_logical_name."""

from unittest import mock

import pytest

from openapi_sqlalchemy import helpers


@pytest.mark.prod_env
@pytest.mark.helper
def test_add_logical_name_exists():
    """
    GIVEN
    WHEN
    THEN helpers has add_logical_name property.
    """
    assert hasattr(helpers, "add_logical_name")


@pytest.mark.prod_env
@pytest.mark.helper
def test_add_logical_name_call(args, kwargs):
    """
    GIVEN mock function, args and kwargs
    WHEN mock function is decorated with add_logical_name and called with args and
        kwargs
    THEN mock function is called with args and kwargs.
    """
    mock_func = mock.MagicMock()

    decorated = helpers.add_logical_name(mock_func)
    decorated(*args, logical_name="name 1", **kwargs)

    mock_func.assert_called_once_with(*args, **kwargs)


@pytest.mark.prod_env
@pytest.mark.helper
def test_add_logical_name_return():
    """
    GIVEN mock function and logical name
    WHEN mock function is decorated with add_logical_name and called
    THEN the return value is the mock function return value in a dictionary with the
        logical name as key.
    """
    mock_func = mock.MagicMock()

    decorated = helpers.add_logical_name(mock_func)
    return_value = decorated(logical_name="name 1")

    assert return_value == {"name 1": mock_func.return_value}
