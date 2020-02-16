"""Resolve $ref and merge allOf."""

from open_alchemy import types

from . import ref
from .merge_all_of import merge_all_of


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
    return merge_all_of(schema=schema, schemas=schemas)
