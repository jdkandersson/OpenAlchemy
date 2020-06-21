"""Functions to convert to dictionary."""

import typing

from ... import exceptions
from ... import helpers
from ... import types as oa_types
from .. import types
from . import array
from . import object_
from . import simple


def convert(*, schema: oa_types.Schema, value: typing.Any) -> types.TAnyDict:
    """
    Convert value for a schema to a dictionary.

    Args:
        value: The value to convert.
        schema: The schema of the value.

    Returns:
        The converted value.

    """
    json = helpers.peek.json(schema=schema, schemas={})
    if json:
        return value
    type_ = helpers.peek.type_(schema=schema, schemas={})
    if type_ == "object":
        return object_.convert(value, schema=schema)
    if type_ == "array":
        return array.convert(value, schema=schema)
    if type_ in {"integer", "number", "string", "boolean"}:
        return simple.convert(value, schema=schema)
    raise exceptions.FeatureNotImplementedError(f"Type {type_} is not supported.")


def return_none(*, schema: oa_types.Schema, property_name: str) -> bool:
    """
    Check whether a null value for a property should be returned.

    Assume the schema has properties and that it has a schema for the property.
    Assume that any $ref and allOf has already been resolved.

    The rules are:
    1. if the property is required, return it,
    2. if the property is nullable, return it and
    3. else, don't return it.

    Args:
        schema: The schema for the model.
        property_name: The name of the property to check for.

    Returns:
        Whether the none value should be returned for the property.

    """
    # Retrieve input
    required_array = schema.get("required", None)
    property_schema = schema["properties"][property_name]

    # Check for required and nullable
    if required_array is not None and property_name in set(required_array):
        return True
    nullable_value = helpers.peek.nullable(schema=property_schema, schemas={})
    if nullable_value is True:
        return True
    return False
