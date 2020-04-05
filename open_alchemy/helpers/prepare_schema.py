"""Resolve $ref and merge allOf."""

from open_alchemy import types

from . import all_of
from . import ref


def prepare_schema(*, schema: types.Schema, schemas: types.Schemas) -> types.Schema:
    """
    Resolve $ref and merge allOf.

    Args:
        schema: The schema to prepare.
        schemas: The schemas from which to resolve $ref.

    Returns:
        The prepared schema.

    """
    _, schema = ref.resolve(name="", schema=schema, schemas=schemas)
    return all_of.merge(schema=schema, schemas=schemas)
