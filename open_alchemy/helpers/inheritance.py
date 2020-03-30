"""Helpers to support inheritance."""

# from .. import exceptions
# from .. import types
# from . import schema as schema_helper


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
#     schema = schemas.get(name)
#     if schema is None:
#         raise exceptions.SchemaNotFoundError(
#             f"Could not find the schema {name}."
#         )
#     if not schema_helper.constructable(schema=schema, schemas=schemas):
#         raise exceptions.MalformedSchemaError(
#             f"The schema {name} is not a schema that can be constructed as a model."
#         )
