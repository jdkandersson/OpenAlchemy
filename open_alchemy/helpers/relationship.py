"""Helper functions for relationships."""

import typing

from .. import types
from . import peek
from . import property_
from . import ref


def calculate_type(
    *, schema: types.Schema, schemas: types.Schemas
) -> types.RelationshipType:
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
            return types.RelationshipType.ONE_TO_ONE
        return types.RelationshipType.MANY_TO_ONE

    # Retrieve the items schema
    items_schema = peek.items(schema=schema, schemas=schemas)
    assert items_schema is not None
    secondary = peek.secondary(schema=items_schema, schemas=schemas)
    if secondary is not None:
        return types.RelationshipType.MANY_TO_MANY
    return types.RelationshipType.ONE_TO_MANY


def get_ref_schema_many_to_x(
    *, property_schema: types.Schema, schemas: types.Schemas
) -> typing.Tuple[str, types.Schema]:
    """
    Get the schema referenced by a many-to-x relationship property.

    Assume the schema and schemas are valid.
    Assume the property schema is a many-to-x relationship property.

    Args:
        property_schema: The schema of the many-to-x relationship property.
        schemas: All defined schemas.

    Returns:
        The schema referenced in the many-to-x relationship.

    """
    items_schema = peek.items(schema=property_schema, schemas=schemas)
    assert items_schema is not None
    ref_value = peek.ref(schema=items_schema, schemas=schemas)
    assert ref_value is not None
    return ref.get_ref(ref=ref_value, schemas=schemas)


def is_relationship_type(
    *, type_: types.RelationshipType, schema: types.Schema, schemas: types.Schemas
) -> bool:
    """
    Check whether a property is a relationship of a particular type.

    Args:
        type_: The type of relationship to look for.
        schema: The schema of the property to check.
        schemas: All defined schemas.

    Returns:
        Whether the property is a relationship of a particular type.

    """
    property_type = property_.calculate_type(schema=schema, schemas=schemas)
    if property_type != types.PropertyType.RELATIONSHIP:
        return False

    relationship_type = calculate_type(schema=schema, schemas=schemas)
    return relationship_type == type_
