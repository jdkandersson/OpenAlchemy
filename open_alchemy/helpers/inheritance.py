"""Helpers to support inheritance."""

# from .. import types
# from . import ref


# def check_parent(
#     *, name: types.Schema, parent_name: str, schemas: types.Schemas
# ) -> bool:
#     """
#     Check that the parent is in the inheritance chain of a schema.

#     Raise MalformedSchemaError if the parent is not found in the chain.
#     Raise MalformedSchemaError if the parent does not have x-tablename nor x-inherits.

#     Args:
#         schema: The schema to check.
#         parent_name: The parent to check for in the inheritance chain.
#         schemas: All the schemas.

#     Returns:
#         Whether the parent is in the inheritance chain.

#     """
#     ref = schema.get("$ref")
#     all_of = schema.get("allOf")

#     if ref is None and all_of is None:
#         raise
