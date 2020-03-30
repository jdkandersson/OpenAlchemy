"""Helpers to support inheritance."""

from .. import exceptions
from .. import types
from . import ref as ref_helper
from . import schema as schema_helper


def check_parent(
    *, schema: types.Schema, parent_name: str, schemas: types.Schemas
) -> bool:
    """
    Check that the parent is in the inheritance chain of a schema.

    Raise MalformedSchemaError if the parent is not found in the chain.
    Raise MalformedSchemaError if the parent does not have x-tablename nor x-inherits.

    Args:
        schema: The schema to check.
        parent_name: The parent to check for in the inheritance chain.
        schemas: All the schemas.

    Returns:
        Whether the parent is in the inheritance chain.

    """
    # Check for $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")
    if ref is None and all_of is None:
        return False

    # Handle $ref
    if ref is not None:
        ref_name, ref_schema = ref_helper.get_ref(ref=ref, schemas=schemas)

        # Check for name match base case
        if ref_name == parent_name:
            return schema_helper.constructable(schema=ref_schema, schemas=schemas)

        # Recursive case
        return check_parent(schema=ref_schema, parent_name=parent_name, schemas=schemas)

    # Handle allOf
    if not isinstance(all_of, list):
        raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
    return any(
        check_parent(schema=sub_schema, parent_name=parent_name, schemas=schemas)
        for sub_schema in all_of
    )
