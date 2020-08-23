"""Retrieve model artifacts."""

import typing

from ... import helpers as oa_helpers
from ... import table_args
from ... import types as oa_types
from . import types


def get(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.ModelArtifacts:
    """
    Retrieve the artifacts for the model.

    Assume that the schema is valid.

    Args:
        schema: The model schema.
        schemas: All the defined schemas used to resolve any $ref.

    Returns:
        The artifacts for the model.

    """
    tablename = oa_helpers.peek.tablename(schema=schema, schemas=schemas)
    assert tablename is not None
    inherits = oa_helpers.schema.inherits(schema=schema, schemas=schemas)
    parent: typing.Optional[str] = None
    if inherits is True:
        parent = oa_helpers.inheritance.get_parent(schema=schema, schemas=schemas)

    description = oa_helpers.peek.description(schema=schema, schemas=schemas)

    mixins = oa_helpers.peek.mixins(schema=schema, schemas=schemas)

    kwargs = oa_helpers.peek.kwargs(schema=schema, schemas=schemas)

    composite_index: typing.Optional[oa_types.IndexList] = None
    composite_index_value = oa_helpers.peek.composite_index(
        schema=schema, schemas=schemas
    )
    if composite_index_value is not None:
        composite_index = table_args.factory.map_index(spec=composite_index_value)

    composite_unique: typing.Optional[oa_types.UniqueList] = None
    composite_unique_value = oa_helpers.peek.composite_unique(
        schema=schema, schemas=schemas
    )
    if composite_unique_value is not None:
        composite_unique = table_args.factory.map_unique(spec=composite_unique_value)

    return types.ModelArtifacts(
        tablename=tablename,
        inherits=inherits,
        parent=parent,
        description=description,
        mixins=mixins,
        kwargs=kwargs,
        composite_index=composite_index,
        composite_unique=composite_unique,
    )
