"""Construct table args for a model."""

import itertools
import typing

from sqlalchemy import schema as sa_schema

from open_alchemy import types
from open_alchemy.helpers import ext_prop

from . import factory

TableArg = typing.Union[sa_schema.UniqueConstraint, sa_schema.Index]
TableArgs = typing.Tuple[TableArg, ...]


def construct(*, schema: types.Schema) -> TableArgs:
    """
    Construct any table args from the object schema.

    Look for x-composite-unique and x-composite-index keys in the schema and construct
    any unique constraints and indexes based on their value.

    Args:
        schema: The schema for the object.

    Returns:
        A tuple with any unique constraints and indexes.

    """
    # Keep track of any table arguments
    table_args: typing.List[typing.Iterable[TableArg]] = []

    # Handle x-composite-unique
    unique_spec = ext_prop.get(
        source=schema, name=types.ExtensionProperties.COMPOSITE_UNIQUE
    )
    if unique_spec is not None:
        table_args.append(factory.unique_factory(spec=unique_spec))
    # Handle x-composite-index
    index_spec = ext_prop.get(
        source=schema, name=types.ExtensionProperties.COMPOSITE_INDEX
    )
    if index_spec is not None:
        table_args.append(factory.index_factory(spec=index_spec))

    return tuple(itertools.chain.from_iterable(table_args))
