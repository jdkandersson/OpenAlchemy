"""Helpers for back references."""

import typing

from ... import helpers
from ... import types


def get(schemas: types.Schemas, schema: types.Schema) -> typing.Optional[str]:
    """
    Get the back reference from the property schema.

    The following rules are used:
    1. if there is an items key, recursively call on the items value.
    1. peek for x-backrefs on the schema and return if found.
    3. Return None.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the property.

    Returns:
        Whether the property defines a back reference.

    """
    # Handle items
    items_schema = helpers.peek.items(schema=schema, schemas=schemas)
    if items_schema is not None:
        return get(schema=items_schema, schemas=schemas)

    # Peek for backref
    return helpers.peek.backref(schema=schema, schemas=schemas)


def defined(schemas: types.Schemas, schema: types.Schema) -> bool:
    """
    Check whether the property schema defines a back reference.

    The following rules are used:
    1. if there is an items key, recursively call on the items value.
    1. peek for x-backrefs on the schema and return True if found.
    3. Return False.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the property.

    Returns:
        Whether the property defines a back reference.

    """
    return get(schemas, schema) is not None
