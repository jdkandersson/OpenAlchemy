"""Retrieve artifacts for a simple property."""

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema
) -> types.SimplePropertyArtifacts:
    """
    Retrieve the artifacts for a simple property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the simple property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    format_ = oa_helpers.peek.format_(schema=schema, schemas=schemas)
    max_length = oa_helpers.peek.max_length(schema=schema, schemas=schemas)

    autoincrement = oa_helpers.peek.autoincrement(schema=schema, schemas=schemas)
    kwargs = oa_helpers.peek.kwargs(schema=schema, schemas=schemas)
    foreign_key = oa_helpers.peek.foreign_key(schema=schema, schemas=schemas)
    foreign_key_kwargs = oa_helpers.peek.foreign_key_kwargs(
        schema=schema, schemas=schemas
    )

    return types.SimplePropertyArtifacts(
        type_=helpers.property_.type_.Type.SIMPLE,
        open_api=types.OpenApiSimplePropertyArtifacts(
            type_=type_, format_=format_, max_length=max_length
        ),
        extension=types.ExtensionSimplePropertyArtifacts(
            autoincrement=autoincrement,
            kwargs=kwargs,
            foreign_key=foreign_key,
            foreign_key_kwargs=foreign_key_kwargs,
        ),
    )
