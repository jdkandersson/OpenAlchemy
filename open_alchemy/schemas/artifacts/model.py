"""Retrieve model artifacts."""

import typing

from ... import helpers as oa_helpers
from ... import types as oa_types
from . import types


def get(*, schema: oa_types.Schema, schemas: oa_types.Schemas) -> types.ModelArtifacts:
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

    return types.ModelArtifacts(tablename=tablename, inherits=inherits, parent=parent)
