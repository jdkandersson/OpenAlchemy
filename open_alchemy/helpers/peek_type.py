"""Assemble the final schema and return its type."""

import typing

from open_alchemy import exceptions
from open_alchemy import types

from .resolve_ref import get_ref


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
    type_ = _peek_key(schema=schema, schemas=schemas, key="type")
    if type_ is None:
        raise exceptions.TypeMissingError("Every property requires a type.")
    if not isinstance(type_, str):
        raise exceptions.TypeMissingError(
            "A type property must be defined using a string"
        )
    return type_


def _peek_key(*, schema: types.Schema, schemas: types.Schemas, key: str) -> typing.Any:
    """Recursive type lookup."""
    # Base case, look for type key
    type_ = schema.get(key)
    if type_ is not None:
        return type_

    # Recursive case, look for $ref
    ref = schema.get("$ref")
    if ref is not None:
        _, ref_schema = get_ref(ref=ref, schemas=schemas)
        return _peek_key(schema=ref_schema, schemas=schemas, key=key)

    # Recursive case, look for allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        for sub_schema in all_of:
            type_ = _peek_key(schema=sub_schema, schemas=schemas, key=key)
            if type_ is not None:
                return type_

    # Base case, type or ref not found or no type in allOf
    return None
