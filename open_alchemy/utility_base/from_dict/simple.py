"""Convert simple type from dictionary to the column equivalent."""

import datetime

from ... import exceptions
from ... import helpers
from ... import types as oa_types
from .. import types


def convert(
    value: types.TOptSimpleDict, *, schema: oa_types.Schema
) -> types.TOptSimpleCol:
    """
    Convert simple value from a dictionary to the column equivalent.

    Raises InvalidInstanceError if the value is not of the type implied by the schema.

    Args:
        value: The value to convert.
        schema: The schema for the value.

    Returns:
        The value converted for a column.

    """
    type_ = helpers.peek.type_(schema=schema, schemas={})
    if value is None:
        return None

    if type_ == "integer":
        if not isinstance(value, int):
            raise exceptions.InvalidInstanceError(
                "Integer type columns must have int values."
            )
        return value
    if type_ == "number":
        if not isinstance(value, float):
            raise exceptions.InvalidInstanceError(
                "Number type columns must have float values."
            )
        return value
    if type_ == "string":
        return _handle_string(value, schema=schema)
    if type_ == "boolean":
        if not isinstance(value, bool):
            raise exceptions.InvalidInstanceError(
                "Boolean type columns must have bool values."
            )
        return value

    raise exceptions.FeatureNotImplementedError(f"Type {type_} is not supported.")


def _handle_string(
    value: types.TSimpleDict, *, schema: oa_types.Schema
) -> types.TStringCol:
    """
    Convert string type value to column type.

    Raises InvalidInstanceError if the value is not of the type implied by the schema.

    Args:
        value: The value to convert.

    Returns:
        The converted value.

    """
    if not isinstance(value, str):
        raise exceptions.InvalidInstanceError(
            "String type columns must have str values."
        )
    format_ = helpers.peek.format_(schema=schema, schemas={})
    if format_ == "date":
        return datetime.date.fromisoformat(value)
    if format_ == "date-time":
        return datetime.datetime.fromisoformat(value)
    if format_ == "binary":
        return value.encode()
    return value
