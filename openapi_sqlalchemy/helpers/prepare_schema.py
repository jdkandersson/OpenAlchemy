"""Resolve $ref and merge allOf."""

from openapi_sqlalchemy import types

from .merge_all_of import merge_all_of
from .resolve_ref import resolve_ref


def prepare_schema(*, schema: types.Schema, schemas: types.Schemas) -> types.Schema:
    """
    Resolve $ref and merge allOf.

    Args:
        schema: The schema to prepare.
        schemas: The schemas from which to resolve $ref.

    Returns:
        The prepared schema.

    """
    _, schema = resolve_ref(name="", schema=schema, schemas=schemas)
    return merge_all_of(schema=schema, schemas=schemas)
