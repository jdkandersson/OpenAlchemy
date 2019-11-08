"""Construct table args for a model."""

import itertools
import typing

from sqlalchemy import schema as sa_schema

from open_alchemy import helpers
from open_alchemy import types

from . import factory

TableArgs = typing.Tuple[typing.Union[sa_schema.UniqueConstraint, sa_schema.Index], ...]


def construct(*, schema: types.Schema) -> TableArgs:
    """
    Construct any table args from the object schema.

    Look for x-unique-constraint and x-composite-index keys in the schema and construct
    any unique constraints and indexes based on their value.

    Args:
        schema: The schema for the object.

    Returns:
        A tuple with any unique constraints and indexes.

    """
    # Keep track of any table arguments
    table_args = []

    # Handle x-unique-constraint
    unique_spec = helpers.get_ext_prop(source=schema, name="x-unique-constraint")
    if unique_spec is not None:
        table_args.append(factory.unique_factory(spec=unique_spec))
    # Handle x-composite-index
    index_spec = helpers.get_ext_prop(source=schema, name="x-composite-index")
    if index_spec is not None:
        table_args.append(factory.index_factory(spec=index_spec))

    return tuple(itertools.chain.from_iterable(table_args))
