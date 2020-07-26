"""Functions to expose iterables for schemas."""

import typing

from ... import helpers
from ... import types


def constructable(
    *, schemas: types.Schemas
) -> typing.Iterable[typing.Tuple[str, types.Schema]]:
    """
    Create an iterable with all constructable schemas.

    Args:
        schemas: The schemas to iterate over.

    Returns:
        iterable with all schemas that are constructable.

    """
    for name, schema in schemas.items():
        if not helpers.schema.constructable(schema=schema, schemas=schemas):
            continue

        yield name, schema
