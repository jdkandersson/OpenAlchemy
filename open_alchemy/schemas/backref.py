"""Pre-process schemas by adding any back references into the schemas."""

# import typing

from .. import helpers
from .. import types


def _defines_backref(schema: types.Schema, *, schemas: types.Schemas) -> bool:
    """
    Check whether the property schema defines a back reference.

    The following rules are used:
    1. if there is an items key, recursively call on the items value.
    1. peek for x-backrefs on the schema and return True if found.
    3. Return False.

    Args:
        _: Placeholder for unused name argument.
        schema: The schema of the property.
        schemas: All the defined schemas.

    Returns:
        Whether the property defines a back reference.

    """
    # Handle items
    items_schema = schema.get("items")
    if items_schema is not None:
        return _defines_backref(schema=items_schema, schemas=schemas)

    # Peek for backref
    backref = helpers.peek.backref(schema=schema, schemas=schemas)
    if backref is not None:
        return True

    return False


# def _calculate_schema(
#     schema: types.Schema, *, schema_name: str, schemas: types.Schemas
# ) -> typing.Tuple[str, types.Schema]:
#     """
#     Calculate the schema for a back reference.

#     Args:
#         schema: The schema of a property with a back reference.
#         schema_name: The name of the schema that the property is on.
#         schema: All the defines schemas.

#     Returns:
#         The name of the schema the back reference needs to be added to.

#     """
