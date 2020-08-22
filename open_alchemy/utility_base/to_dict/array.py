"""Convert array to dictionary."""

import functools
import typing

from ... import exceptions
from ... import helpers
from ... import types as ao_types
from .. import types
from . import object_


def convert(value: typing.Any, *, schema: ao_types.Schema) -> types.TOptArrayDict:
    """
    Convert array property so that it can be included in an object dictionary.

    Raises MalformedSchemaError if schema does not define item schema.
    Raises MalformedSchemaError if the item schema is not of type object.
    Raises MalformedSchemaError if the item schema is not of type object.

    Args:
        value: The value to convert.
        schema: The schema for the value.

    Returns:
        The value converted to a list of dictionary.

    """
    if value is None:
        return None
    item_schema = schema.get("items")
    if item_schema is None:
        raise exceptions.MalformedSchemaError(
            "The array item schema must have an items property."
        )
    item_type = helpers.peek.type_(schema=item_schema, schemas={})
    if item_type != "object":
        raise exceptions.FeatureNotImplementedError(
            "The array item schema must be of type object."
        )
    read_only = helpers.peek.read_only(schema=schema, schemas={})
    item_conversion = functools.partial(
        object_.convert, schema=item_schema, read_only=read_only
    )
    try:
        converted_items = map(item_conversion, value)
    except TypeError as exc:
        raise exceptions.InvalidInstanceError("Array values must be iterable.") from exc
    return list(converted_items)
