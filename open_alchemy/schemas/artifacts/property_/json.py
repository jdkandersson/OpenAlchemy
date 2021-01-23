"""Retrieve artifacts for a JSON property."""

import copy

from .... import types as oa_types
from ....helpers import peek
from ....helpers import schema as schema_helper
from ...helpers import clean
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
    schema = copy.deepcopy(schema_helper.prepare_deep(schema=schema, schemas=schemas))

    nullable = peek.nullable(schema=schema, schemas=schemas)

    description = peek.description(schema=schema, schemas=schemas)

    read_only = peek.read_only(schema=schema, schemas=schemas)
    write_only = peek.write_only(schema=schema, schemas=schemas)

    primary_key = peek.primary_key(schema=schema, schemas=schemas)
    index = peek.index(schema=schema, schemas=schemas)
    unique = peek.unique(schema=schema, schemas=schemas)

    foreign_key = peek.foreign_key(schema=schema, schemas=schemas)

    kwargs = peek.kwargs(schema=schema, schemas=schemas)
    foreign_key_kwargs = peek.foreign_key_kwargs(schema=schema, schemas=schemas)

    # Remove extension properties from schema
    clean.extension(schema=schema)
    # Add in x-json
    schema[oa_types.ExtensionProperties.JSON] = True

    return types.JsonPropertyArtifacts(
        type=oa_types.PropertyType.JSON,
        description=description,
        schema=schema,
        required=required,
        open_api=types.OpenApiJsonPropertyArtifacts(
            nullable=nullable,
            read_only=read_only,
            write_only=write_only,
        ),
        extension=types.ExtensionJsonPropertyArtifacts(
            primary_key=primary_key is True,
            index=index,
            unique=unique,
            foreign_key=foreign_key,
            kwargs=kwargs,
            foreign_key_kwargs=foreign_key_kwargs,
        ),
    )
