"""Convert array values to columns."""

import functools

from ... import exceptions
from ... import helpers
from ... import types as oa_types
from .. import types
from . import object_


def convert(
    value: types.TOptArrayDict, *, schema: oa_types.Schema
) -> types.TOptArrayCol:
    """
    Convert array value from a dictionary to a column.

    Raises MalformedSchemaError if the items schema is missing from the schema.
    Raises MalformedSchemaError if the items type is not object.
    Raises InvalidInstanceError if the value is not an iterable.

    Args:
        value: The value to convert.
        schema: The schema of the value.

    Returns:
        The converted value.

    """
    # Check the schema
    items_schema = schema.get("items")
    if items_schema is None:
        raise exceptions.MalformedSchemaError(
            "To construct array parameters the schema for the property "
            "must include the items property with the information about "
            "the array items."
        )
    items_type = helpers.peek.type_(schema=items_schema, schemas={})
    if items_type != "object":
        raise exceptions.MalformedSchemaError(
            "The type of the array items must be object."
        )

    if value is None:
        return None
    # Convert values
    item_conversion = functools.partial(object_.convert, schema=items_schema)
    try:
        converted_items = map(item_conversion, value)
    except TypeError as exc:
        raise exceptions.InvalidInstanceError("Array values must be iterable.") from exc
    return list(converted_items)
