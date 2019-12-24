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
    value = peek_key(schema=schema, schemas=schemas, key="type")
    if value is None:
        raise exceptions.TypeMissingError("Every property requires a type.")
    if not isinstance(value, str):
        raise exceptions.TypeMissingError(
            "A type property value must be of type string."
        )
    return value


def nullable(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the nullable property from a property schema.

    Raises MalformedSchemaError if the nullable value is not a boolean.

    Args:
        schema: The schema to get the nullable from.
        schemas: The schemas for $ref lookup.

    Returns:
        The nullable value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="nullable")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A nullable value must be of type boolean."
        )
    return value


def format_(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the format property from a property schema.

    Raises MalformedSchemaError if the format value is not a string.

    Args:
        schema: The schema to get the format from.
        schemas: The schemas for $ref lookup.

    Returns:
        The format value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="format")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError("A format value must be of type string.")
    return value


def max_length(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[int]:
    """
    Retrieve the maxLength property from a property schema.

    Raises MalformedSchemaError if the maxLength value is not an integer.

    Args:
        schema: The schema to get the maxLength from.
        schemas: The schemas for $ref lookup.

    Returns:
        The maxLength value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="maxLength")
    if value is None:
        return None
    if not isinstance(value, int):
        raise exceptions.MalformedSchemaError(
            "A maxLength value must be of type integer."
        )
    return value


def read_only(*, schema: types.Schema, schemas: types.Schemas) -> bool:
    """
    Determine whether schema is readOnly.

    Raises MalformedSchemaError if the readOnly value is not a boolean.

    Args:
        schema: The schema to get readOnly from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is readOnly.

    """
    value = peek_key(schema=schema, schemas=schemas, key="readOnly")
    if value is None:
        return False
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A readOnly property must be of type boolean."
        )
    return value


def primary_key(*, schema: types.Schema, schemas: types.Schemas) -> bool:
    """
    Determine whether property schema is for a primary key.

    Raises MalformedSchemaError if the x-primary-key value is not a boolean.

    Args:
        schema: The schema to get x-primary-key from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is for a primary key property.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-primary-key")
    if value is None:
        return False
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-primary-key property must be of type boolean."
        )
    return value


def tablename(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the tablename of the schema.

    Raises MalformedSchemaError if the tablename value is not a string.

    Args:
        schema: The schema to get tablename from.
        schemas: The schemas for $ref lookup.

    Returns:
        The tablename or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-tablename")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-tablename property must be of type string."
        )
    return value


def peek_key(*, schema: types.Schema, schemas: types.Schemas, key: str) -> typing.Any:
    """Recursive type lookup."""
    # Base case, look for type key
    value = schema.get(key)
    if value is not None:
        return value

    # Recursive case, look for $ref
    ref = schema.get("$ref")
    if ref is not None:
        _, ref_schema = get_ref(ref=ref, schemas=schemas)
        return peek_key(schema=ref_schema, schemas=schemas, key=key)

    # Recursive case, look for allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        for sub_schema in all_of:
            value = peek_key(schema=sub_schema, schemas=schemas, key=key)
            if value is not None:
                return value

    # Base case, type or ref not found or no type in allOf
    return None
