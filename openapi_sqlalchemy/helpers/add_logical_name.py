"""Adds logical name to column."""

import typing

from .testing_guard import testing_guard


@testing_guard(environment_name="TESTING")
def add_logical_name(func: typing.Callable) -> typing.Callable:
    """
    Convert return value to dictionary with logical_name: <return value>.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function that now expects the logical_name keyword argument an
             passes through any other args and kwargs.

    """

    def replacement(*args, logical_name: str, **kwargs):
        """Replace original function."""
        return_value = func(*args, **kwargs)

        return [(logical_name, return_value)]

    return replacement
