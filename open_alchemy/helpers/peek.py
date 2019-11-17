"""Assemble the final schema and return its type."""

import typing

from open_alchemy import exceptions
from open_alchemy import types

from .resolve_ref import get_ref


def type_(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get the type of the schema.

    Raises TypeMissingError if the final schema does not have a type or the value is
    not a string.

    Args:
        schema: The schema for which to get the type.
        schemas: The schemas for $ref lookup.

    Returns:
        The type of the schema.

    """
    value = _peek_key(schema=schema, schemas=schemas, key="type")
    if value is None:
        raise exceptions.TypeMissingError("Every property requires a type.")
    if not isinstance(value, str):
        raise exceptions.TypeMissingError(
            "A type property value must be of type string."
        )
    return value


def read_only(*, schema: types.Schema, schemas: types.Schemas) -> bool:
    """
    Determine whether schema is readOnly.

    Raises MalformedSchemaError if the readOnly value is not a boolean.

    Args:
        schema: The schema for which to get the type.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is readOnly.

    """
    value = _peek_key(schema=schema, schemas=schemas, key="readOnly")
    if value is None:
        return False
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A readOnly property must be of type boolean."
        )
    return value


def _peek_key(*, schema: types.Schema, schemas: types.Schemas, key: str) -> typing.Any:
    """Recursive type lookup."""
    # Base case, look for type key
    value = schema.get(key)
    if value is not None:
        return value

    # Recursive case, look for $ref
    ref = schema.get("$ref")
    if ref is not None:
        _, ref_schema = get_ref(ref=ref, schemas=schemas)
        return _peek_key(schema=ref_schema, schemas=schemas, key=key)

    # Recursive case, look for allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        for sub_schema in all_of:
            value = _peek_key(schema=sub_schema, schemas=schemas, key=key)
            if value is not None:
                return value

    # Base case, type or ref not found or no type in allOf
    return None
