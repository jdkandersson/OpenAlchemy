"""Convert an OpenAPI value based on the format to the equivalent Python value."""

import datetime
import typing

from open_alchemy import exceptions
from open_alchemy import types


def convert(
    *, value: types.TColumnDefault, type_: str, format_: typing.Optional[str]
) -> types.TPyColumnDefault:
    """
    Convert an OpenAPI value to it's python type based on the format.

    Args:
        value: The value to convert.
        type_: The OpenAPI type.
        format_: The OpenAPI format.

    Returns:
        The value converted to its equivalent Python type.

    """
    if type_ in {"object", "array"}:
        raise exceptions.MalformedSchemaError(
            "Cannot convert object nor array types to Python equivalent values."
        )

    if isinstance(value, str) and format_ == "date":
        try:
            return datetime.date.fromisoformat(value)
        except ValueError as exc:
            raise exceptions.MalformedSchemaError("Invalid date string.") from exc
    if isinstance(value, str) and format_ == "date-time":
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError as exc:
            raise exceptions.MalformedSchemaError("Invalid date-time string.") from exc
    if isinstance(value, str) and format_ == "binary":
        return value.encode()
    if format_ == "double":
        raise exceptions.MalformedSchemaError("Double format is not supported.")
    return value
