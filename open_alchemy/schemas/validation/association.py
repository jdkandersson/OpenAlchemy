"""Validate association tables."""

import typing

from ... import helpers as oa_helpers
from ... import types
from .. import helpers


def _get_defined_association_iterator(
    *, schemas: types.Schemas, tablename_mapping: typing.Dict[str, typing.Any]
) -> typing.Iterable[typing.Tuple[str, types.Schema]]:
    """
    Get an iterator with schemas that have a tablename as defined by a mapping.

    Assume that individual schemas are valid.

    Algorithm:
    1. iterate over constructable schemas
    2. include any with an x-tablename value that appears in the tablename mapping

    Args:
        schemas: All defined schemas.
        tablename_mapping: A mapping of tablename to some value. Keys are used to
            indicate to include a schema.

    Returns:
        An iterator with all schemas that have their x-tablename appear in the
        tablename mapping.

    """
    constructables = helpers.iterate.constructable(schemas=schemas)
    return filter(
        lambda args: oa_helpers.peek.tablename(schema=args[1], schemas=schemas)
        in tablename_mapping,
        constructables,
    )


# def validate_schema(*, name: str, schema: types.Schema, )
