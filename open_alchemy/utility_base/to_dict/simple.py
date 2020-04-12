"""Convert simple types (not object nor array)."""

import typing

from ... import exceptions
from ... import helpers
from ... import types as oa_types
from .. import types


def convert(value: typing.Any, *, schema: oa_types.Schema) -> types.TOptSimpleDict:
    """
    Convert values with basic types to dictionary values.

    Args:
        value: The value to convert.
        schema: The schema for the value.

    Returns:
        The value converted to the expected dictionary value.

    """
    type_ = helpers.peek.type_(schema=schema, schemas={})
    if type_ not in {"integer", "number", "string", "boolean"}:
        raise exceptions.FeatureNotImplementedError(f"Type {type_} is not supported.")
    format_ = helpers.peek.format_(schema=schema, schemas={})
    if format_ == "date":
        return value.isoformat()
    if format_ == "date-time":
        return value.isoformat()
    if format_ == "binary":
        return value.decode()
    return value
