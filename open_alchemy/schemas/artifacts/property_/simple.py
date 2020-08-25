"""Retrieve artifacts for a simple property."""

import copy

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
    schema = copy.deepcopy(oa_helpers.schema.prepare(schema=schema, schemas=schemas))

    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    format_ = oa_helpers.peek.format_(schema=schema, schemas=schemas)
    max_length = oa_helpers.peek.max_length(schema=schema, schemas=schemas)
    nullable = oa_helpers.peek.nullable(schema=schema, schemas=schemas)

    description = oa_helpers.peek.description(schema=schema, schemas=schemas)

    default = oa_helpers.peek.default(schema=schema, schemas=schemas)

    read_only = oa_helpers.peek.read_only(schema=schema, schemas=schemas)
    write_only = oa_helpers.peek.write_only(schema=schema, schemas=schemas)

    primary_key = oa_helpers.peek.primary_key(schema=schema, schemas=schemas)
    autoincrement = oa_helpers.peek.autoincrement(schema=schema, schemas=schemas)
    index = oa_helpers.peek.index(schema=schema, schemas=schemas)
    unique = oa_helpers.peek.unique(schema=schema, schemas=schemas)

    foreign_key = oa_helpers.peek.foreign_key(schema=schema, schemas=schemas)

    kwargs = oa_helpers.peek.kwargs(schema=schema, schemas=schemas)
    foreign_key_kwargs = oa_helpers.peek.foreign_key_kwargs(
        schema=schema, schemas=schemas
    )

    # Remove extension properties from schema
    properties = [
        "x-primary-key",
        "x-index",
        "x-unique",
        "x-foreign-key",
        "x-kwargs",
        "x-foreign-key-kwargs",
    ]
    for prop in properties:
        if prop not in schema:
            continue
        del schema[prop]

    return types.SimplePropertyArtifacts(
        type_=helpers.property_.type_.Type.SIMPLE,
        schema=schema,
        open_api=types.OpenApiSimplePropertyArtifacts(
            type_=type_,
            format_=format_,
            max_length=max_length,
            nullable=nullable,
            description=description,
            default=default,
            read_only=read_only,
            write_only=write_only,
        ),
        extension=types.ExtensionSimplePropertyArtifacts(
            primary_key=primary_key,
            autoincrement=autoincrement,
            index=index,
            unique=unique,
            foreign_key=foreign_key,
            kwargs=kwargs,
            foreign_key_kwargs=foreign_key_kwargs,
        ),
    )
