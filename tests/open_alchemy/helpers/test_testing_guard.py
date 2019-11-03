"""Tests for testing_guard helper."""

import json
import os
from unittest import mock

import pytest

from open_alchemy.helpers.testing_guard import testing_guard


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_not_set_decorated_call(args, kwargs):
    """
    GIVEN TESTING environment variable is not set, mock decorator and args and
        kwargs
    WHEN decorator is applied to a function after decorating it with the
        testing guard and calling the decorated function with args and kwargs
    THEN decorator return value is called with args and kwargs.
    """
    # Defining mock decorator
    mock_decorator = mock.MagicMock()

    # Decorating with testing guard and calling
    guarded_mock_decorator = testing_guard(environment_name="TESTING")(mock_decorator)
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock.MagicMock())
    # Calling function
    mock_decorated_func(*args, **kwargs)

    # Checking decorator call
    mock_decorator.return_value.assert_called_once_with(*args, **kwargs)


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_not_set_return():
    """
    GIVEN TESTING environment variable is not set and mock decorator
    WHEN decorator is applied to a function after decorating it with the
        testing guard and calling the decorated function
    THEN the return value is the decorator's return value return value.
    """
    # Defining mock decorator
    mock_decorator = mock.MagicMock()

    # Decorating with testing guard and calling
    guarded_mock_decorator = testing_guard(environment_name="TESTING")(mock_decorator)
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock.MagicMock())
    # Calling function
    return_value = mock_decorated_func()

    # Checking decorator call
    assert return_value == mock_decorator.return_value.return_value


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_not_set_func_call():
    """
    GIVEN TESTING environment variable is not set and mock function
    WHEN a decorator is applied to the function after decorating it with the
        testing guard and calling the decorated function
    THEN function is not called.
    """
    # Defining mock decorator
    mock_func = mock.MagicMock()

    # Decorating with testing guard and calling
    mock_decorator = mock.MagicMock()
    guarded_mock_decorator = testing_guard(environment_name="TESTING")(mock_decorator)
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock_func)
    # Calling function
    mock_decorated_func()

    # Checking decorator call
    mock_func.assert_not_called()


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_set_env_name_decorated_call(monkeypatch):
    """
    GIVEN different testing environment variable is set and mock decorator
    WHEN decorator is applied to a function after decorating it with the
        testing guard and calling the decorated function
    THEN decorator return value is not called.
    """
    # Adding TESTING environment variable
    monkeypatch.setenv("DIFFERENT_TESTING", "")
    # Defining mock decorator
    mock_decorator = mock.MagicMock(name="mock_decorator")

    def mock_decorator_func(*args, **kwargs):
        return mock_decorator(*args, **kwargs)

    # Decorating with testing guard and calling
    guarded_mock_decorator = testing_guard(environment_name="DIFFERENT_TESTING")(
        mock_decorator_func
    )
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock.MagicMock(name="mock_func"))
    # Calling function
    mock_decorated_func()

    # Checking decorator call
    mock_decorator.return_value.assert_not_called()


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_set_func_call(monkeypatch, args, kwargs):
    """
    GIVEN TESTING environment variable is set, mock function and args and
        kwargs
    WHEN a decorator is applied to the function after decorating it with the
        testing guard and calling the decorated function with args and kwargs
    THEN function is called with args and kwargs.
    """
    # Adding TESTING environment variable
    monkeypatch.setenv("TESTING", "")
    # Defining mock decorator
    mock_func = mock.MagicMock()

    # Decorating with testing guard and calling
    mock_decorator = mock.MagicMock()

    def mock_decorator_func(*args, **kwargs):
        return mock_decorator(*args, **kwargs)

    guarded_mock_decorator = testing_guard(environment_name="TESTING")(
        mock_decorator_func
    )
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock_func)
    # Calling function
    mock_decorated_func(*args, **kwargs)

    # Checking decorator call
    mock_func.assert_called_once_with(*args, **kwargs)


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_set_decorator_trace_no_closures(monkeypatch):
    """
    GIVEN TESTING and DECORATOR_TRACE environment variable is set and a mock function
        and decorator that doesn't have any closures
    WHEN the decorator is applied to the function after decorating it with the
        testing guard and calling the decorated function
    THEN the function name and None clusres are recorded in the DECORATOR_TRACE
        environment variable.
    """
    # Adding TESTING and DECORATOR_TRACE environment variable
    monkeypatch.setenv("TESTING", "")
    monkeypatch.setenv("DECORATOR_TRACE", json.dumps([]))
    # Defining mock decorator
    mock_func = mock.MagicMock()

    # Decorating with testing guard and calling

    def mock_decorator(*_args, **_kwargs):
        pass

    guarded_mock_decorator = testing_guard(environment_name="TESTING")(mock_decorator)
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock_func)
    # Calling function
    mock_decorated_func()

    # Checking DECORATOR_TRACE addition
    traces = json.loads(os.getenv("DECORATOR_TRACE"))
    assert traces
    trace = traces[0]
    assert "mock_decorator" in trace["function_name"]
    assert trace["closures"] is None


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_set_decorator_trace_closures(monkeypatch):
    """
    GIVEN TESTING and DECORATOR_TRACE environment variable is set and a mock function
        and decorator with closures
    WHEN the decorator is applied to the function after decorating it with the
        testing guard and calling the decorated function
    THEN the function name and None clusres are recorded in the DECORATOR_TRACE
        environment variable.
    """
    # Adding TESTING and DECORATOR_TRACE environment variable
    monkeypatch.setenv("TESTING", "")
    monkeypatch.setenv("DECORATOR_TRACE", json.dumps([]))
    # Defining mock decorator
    mock_func = mock.MagicMock()

    # Decorating with testing guard and calling

    def mock_outer(arg1):
        def mock_decorator(*_args, **_kwargs):
            arg1  # pylint: disable=pointless-statement

        return mock_decorator

    guarded_mock_decorator = testing_guard(environment_name="TESTING")(
        mock_outer(arg1="value 1")
    )
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock_func)
    # Calling function
    mock_decorated_func()

    # Checking DECORATOR_TRACE addition
    traces = json.loads(os.getenv("DECORATOR_TRACE"))
    assert traces
    trace = traces[0]
    assert "mock_decorator" in trace["function_name"]
    assert trace["closures"] == ["value 1"]


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_set_decorator_trace_not_set(monkeypatch):
    """
    GIVEN TESTING is set and DECORATOR_TRACE is not set and mock function
    WHEN a decorator is applied to the function after decorating it with the
        testing guard and calling the decorated function
    THEN DECORATOR_TRACE is still not set.
    """
    # Adding TESTING and DECORATOR_TRACE environment variable
    monkeypatch.setenv("TESTING", "")
    # Defining mock decorator
    mock_func = mock.MagicMock(environment_name="TESTING")

    # Decorating with testing guard and calling
    mock_decorator = mock.MagicMock()
    guarded_mock_decorator = testing_guard(environment_name="TESTING")(mock_decorator)
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock_func)
    # Calling function
    mock_decorated_func()

    # Checking DECORATOR_TRACE addition
    assert os.getenv("DECORATOR_TRACE") is None


@pytest.mark.prod_env
@pytest.mark.helper
def test_testing_guard_set_return(monkeypatch):
    """
    GIVEN TESTING environment variable is set and mock function
    WHEN a decorator is applied to the function after decorating it with the
        testing guard and calling the decorated function
    THEN the return value is the function return value.
    """
    # Adding TESTING environment variable
    monkeypatch.setenv("TESTING", "")
    # Defining mock function
    mock_func = mock.MagicMock()

    # Decorating with testing guard and calling
    mock_decorator = mock.MagicMock()

    def mock_decorator_func(*args, **kwargs):
        return mock_decorator(*args, **kwargs)

    guarded_mock_decorator = testing_guard(environment_name="TESTING")(
        mock_decorator_func
    )
    # Applying decorator
    mock_decorated_func = guarded_mock_decorator(mock_func)
    # Calling function
    return_value = mock_decorated_func()

    # Checking decorator call
    assert return_value == mock_func.return_value
