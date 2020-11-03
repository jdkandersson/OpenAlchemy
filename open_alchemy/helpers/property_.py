"""Helpers to determine the type of a schema."""

from .. import types
from . import peek
from . import type_


def calculate_type(
    *, schemas: types.Schemas, schema: types.Schema
) -> types.PropertyType:
    """
    Calculate the type of the property.

    Assume the property has a valid type.

    The rules are:
    1. if x-json is True it is JSON,
    2. if the type is integer, number, string or boolean it is SIMPLE,
    3. if readOnly is true it is BACKREF and
    4. otherwise it is RELATIONSHIP.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The schema to calculate the type for.

    Returns:
        The type of the property.

    """
    json_value = peek.json(schema=schema, schemas=schemas)
    if json_value is True:
        return types.PropertyType.JSON

    property_type = peek.type_(schema=schema, schemas=schemas)
    if property_type in type_.SIMPLE_TYPES:
        return types.PropertyType.SIMPLE

    read_only_value = peek.read_only(schema=schema, schemas=schemas)
    if read_only_value is True:
        return types.PropertyType.BACKREF

    return types.PropertyType.RELATIONSHIP
