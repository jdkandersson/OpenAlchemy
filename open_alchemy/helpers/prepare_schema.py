"""Resolve $ref and merge allOf."""

import typing

from open_alchemy import types

from . import all_of
from . import ref


def prepare_schema(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    skip_name: typing.Optional[str] = None,
) -> types.Schema:
    """
    Resolve $ref and merge allOf.

    Args:
        schema: The schema to prepare.
        schemas: The schemas from which to resolve $ref.
        skip_name (optional): Any schema name to skip.

    Returns:
        The prepared schema.

    """
    _, schema = ref.resolve(
        name="", schema=schema, schemas=schemas, skip_name=skip_name
    )
    return all_of.merge(schema=schema, schemas=schemas, skip_name=skip_name)
