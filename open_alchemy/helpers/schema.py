"""Helpers for schemas."""

import typing

from .. import types
from . import peek


def constructable(*, schema: types.Schema, schemas: types.Schemas) -> bool:
    """
    Check that a schema is constructable.

    The rules are:
    1. the resolved schema must have either x-tablename or x-inherits and
    2. the schema cannot just be a local $ref.

    Args:
        schema: The schema to check.

    Returns:
        Whether the schema is constructable.

    """
    # Check for reference only models
    ref = schema.get("$ref")
    if ref is not None and ref.startswith("#"):
        return False
    # Check for single item allOf
    all_of = schema.get("allOf")
    if all_of is not None and len(all_of) < 2:
        return False
    # Check for tablename
    if peek.tablename(schema=schema, schemas=schemas) is not None:
        return True
    # Check for inherits
    if inherits(schema=schema, schemas=schemas) is True:
        return True
    return False


def inherits(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Check whether a schema inherits.

    Args:
        schema: The schema to check.
        schemas: All the schemas.

    Returns:
        Whether the schema inherits.

    """
    inherits_value = peek.inherits(schema=schema, schemas=schemas)
    if inherits_value is None:
        return None
    if isinstance(inherits_value, str) or inherits_value is True:
        return True
    return False
