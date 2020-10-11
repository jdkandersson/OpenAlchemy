"""Helpers for relationship properties."""

from .... import helpers
from .... import types


def get_ref_schema_many_to_x(
    *, property_schema: types.Schema, schemas: types.Schemas
) -> types.Schema:
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
    items_schema = helpers.peek.items(schema=property_schema, schemas=schemas)
    assert items_schema is not None
    ref = helpers.peek.ref(schema=items_schema, schemas=schemas)
    assert ref is not None
    _, ref_schema = helpers.ref.get_ref(ref=ref, schemas=schemas)
    return ref_schema
