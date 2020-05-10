"""Convert simple types (not object nor array)."""

import datetime

from ... import exceptions
from ... import helpers
from ... import types as oa_types
from .. import types


def convert(
    value: types.TOptSimpleCol, *, schema: oa_types.Schema
) -> types.TOptSimpleDict:
    """
    Convert values with basic types to dictionary values.

    Raises InvalidInstanceError if the value is not of the type implied by the schema.

    Args:
        value: The value to convert.
        schema: The schema for the value.

    Returns:
        The value converted to the expected dictionary value.

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


def _handle_string(value: types.TSimpleCol, *, schema: oa_types.Schema) -> str:
    """
    Convert string type column to str.

    Raises InvalidInstanceError if the value is not of the type implied by the schema.

    Args:
        value: The value to convert.

    Returns:
        The converted value.

    """
    format_ = helpers.peek.format_(schema=schema, schemas={})
    if format_ == "date":
        if not isinstance(value, datetime.date):
            raise exceptions.InvalidInstanceError(
                "String type columns with date format must have date values."
            )
        return value.isoformat()
    if format_ == "date-time":
        if not isinstance(value, datetime.datetime):
            raise exceptions.InvalidInstanceError(
                "String type columns with date-time format must have datetime "
                "values."
            )
        return value.isoformat()
    if format_ == "binary":
        if not isinstance(value, bytes):
            raise exceptions.InvalidInstanceError(
                "String type columns with binary format must have bytes values."
            )
        return value.decode()
    if not isinstance(value, str):
        raise exceptions.InvalidInstanceError(
            "String type columns must have str values."
        )
    return value
