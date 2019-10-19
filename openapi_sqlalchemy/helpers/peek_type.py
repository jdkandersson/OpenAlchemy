"""Assemble the final schema and return its type."""

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import types

from .prepare_schema import prepare_schema


def peek_type(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get the type of the schema.

    Raises TypeMissingError if the final schema does not have a type.

    Args:
        schema: The schema for which to get the type.
        schemas: The schemas for $ref lookup.

    Returns:
        The type of the schema.

    """
    schema = prepare_schema(schema=schema, schemas=schemas)
    type_ = schema.get("type")
    if type_ is None:
        raise exceptions.TypeMissingError("Every property requires a type.")
    return type_
