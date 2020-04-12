"""Convert simple types (not object nor array)."""

import typing

from .. import types


def convert(
    *, format_: typing.Optional[str], value: typing.Any
) -> types.TOptSimpleDict:
    """
    Convert values with basic types to dictionary values.

    Args:
        format_: The format of the value.
        value: The value to convert.

    Returns:
        The value converted to the expected dictionary value.

    """
    # Handle other types
    if format_ == "date":
        return value.isoformat()
    if format_ == "date-time":
        return value.isoformat()
    if format_ == "binary":
        return value.decode()
    return value
