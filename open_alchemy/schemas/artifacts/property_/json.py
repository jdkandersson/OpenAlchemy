"""Retrieve artifacts for a JSON property."""

import copy

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema, required: bool = False
) -> types.JsonPropertyArtifacts:
    """
    Retrieve the artifacts for a JSON property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the JSON property to gather artifacts for.
        required: WHether the property appears in the required list.

    Returns:
        The artifacts for the property.

    """
    schema = copy.deepcopy(
        oa_helpers.schema.prepare_deep(schema=schema, schemas=schemas)
    )

    nullable = oa_helpers.peek.nullable(schema=schema, schemas=schemas)

    description = oa_helpers.peek.description(schema=schema, schemas=schemas)

    read_only = oa_helpers.peek.read_only(schema=schema, schemas=schemas)
    write_only = oa_helpers.peek.write_only(schema=schema, schemas=schemas)

    primary_key = oa_helpers.peek.primary_key(schema=schema, schemas=schemas)
    index = oa_helpers.peek.index(schema=schema, schemas=schemas)
    unique = oa_helpers.peek.unique(schema=schema, schemas=schemas)

    foreign_key = oa_helpers.peek.foreign_key(schema=schema, schemas=schemas)

    kwargs = oa_helpers.peek.kwargs(schema=schema, schemas=schemas)
    foreign_key_kwargs = oa_helpers.peek.foreign_key_kwargs(
        schema=schema, schemas=schemas
    )

    # Remove extension properties from schema
    helpers.clean.extension(schema=schema)

    return types.JsonPropertyArtifacts(
        type=helpers.property_.type_.Type.JSON,
        description=description,
        schema=schema,
        required=required,
        open_api=types.OpenApiJsonPropertyArtifacts(
            nullable=nullable,
            read_only=read_only,
            write_only=write_only,
        ),
        extension=types.ExtensionJsonPropertyArtifacts(
            primary_key=primary_key,
            index=index,
            unique=unique,
            foreign_key=foreign_key,
            kwargs=kwargs,
            foreign_key_kwargs=foreign_key_kwargs,
        ),
    )
