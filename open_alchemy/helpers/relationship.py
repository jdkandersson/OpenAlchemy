"""Helper functions for relationships."""

import enum

from .. import types
from . import peek


@enum.unique
class Type(str, enum.Enum):
    """The relationship type."""

    MANY_TO_ONE = "MANY_TO_ONE"
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_MANY = "MANY_TO_MANY"


def calculate_type(*, schema: types.Schema, schemas: types.Schemas) -> Type:
    """
    Calculate the type of the relationship the schema defines.

    Assume that the property is a relationship.
    Assume that the property schema has been verified.

    Args:
        schema: The schema of the property.
        schemas: All defined schemas used to resolve any $ref.

    Returns:
        The type of relationship that is defined.

    """
    # Calculate the type of the property
    type_ = peek.type_(schema=schema, schemas=schemas)

    # Handle object
    if type_ == "object":
        # Retrieve uselist
        uselist = peek.prefer_local(
            get_value=peek.uselist, schema=schema, schemas=schemas
        )
        if uselist is False:
            return Type.ONE_TO_ONE
        return Type.MANY_TO_ONE

    # Retrieve the items schema
    items_schema = peek.items(schema=schema, schemas=schemas)
    assert items_schema is not None
    secondary = peek.secondary(schema=items_schema, schemas=schemas)
    if secondary is not None:
        return Type.MANY_TO_MANY
    return Type.ONE_TO_MANY
