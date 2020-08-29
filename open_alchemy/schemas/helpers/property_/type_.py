"""Helpers to determine the type of a schema."""

import enum

from .... import helpers
from .... import types
from . import simple


@enum.unique
class Type(str, enum.Enum):
    """The type of a property."""

    SIMPLE = "SIMPLE"
    JSON = "JSON"
    RELATIONSHIP = "RELATIONSHIP"
    BACKREF = "BACKREF"


def calculate(schemas: types.Schemas, schema: types.Schema) -> Type:
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
    json_value = helpers.peek.json(schema=schema, schemas=schemas)
    if json_value is True:
        return Type.JSON

    type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    if type_ in simple.TYPES:
        return Type.SIMPLE

    read_only_value = helpers.peek.read_only(schema=schema, schemas=schemas)
    if read_only_value is True:
        return Type.BACKREF

    return Type.RELATIONSHIP
