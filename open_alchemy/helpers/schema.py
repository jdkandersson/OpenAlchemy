"""Helpers for schemas."""

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
    inherits = peek.inherits(schema=schema, schemas=schemas)
    if isinstance(inherits, str) or inherits is True:
        return True
    return False
