"""Retrieve artifacts for a simple property."""

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema, required: bool
) -> types.SimplePropertyArtifacts:
    """
    Retrieve the artifacts for a simple property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the simple property to gather artifacts for.
        required: WHether the property appears in the required list.

    Returns:
        The artifacts for the property.

    """
    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    format_ = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.format_, schema=schema, schemas=schemas
    )
    max_length = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.max_length, schema=schema, schemas=schemas
    )
    nullable = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.nullable, schema=schema, schemas=schemas
    )

    description = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.description, schema=schema, schemas=schemas
    )

    default = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.default, schema=schema, schemas=schemas
    )

    read_only = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.read_only, schema=schema, schemas=schemas
    )
    write_only = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.write_only, schema=schema, schemas=schemas
    )

    primary_key = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.primary_key, schema=schema, schemas=schemas
    )
    autoincrement = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.autoincrement, schema=schema, schemas=schemas
    )
    index = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.index, schema=schema, schemas=schemas
    )
    unique = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.unique, schema=schema, schemas=schemas
    )

    foreign_key = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.foreign_key, schema=schema, schemas=schemas
    )

    kwargs = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.kwargs, schema=schema, schemas=schemas
    )
    foreign_key_kwargs = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.foreign_key_kwargs, schema=schema, schemas=schemas
    )

    dict_ignore = oa_helpers.peek.dict_ignore(schema=schema, schemas=schemas)

    # Generate the schema
    schema_artifact: oa_types.ColumnSchema = {
        "type": type_,
    }
    if format_ is not None:
        schema_artifact["format"] = format_
    if max_length is not None:
        schema_artifact["maxLength"] = max_length
    if description is not None:
        schema_artifact["description"] = description
    if nullable is not None:
        schema_artifact["nullable"] = nullable
    if default is not None:
        schema_artifact["default"] = default
    if read_only is not None:
        schema_artifact["readOnly"] = read_only
    if write_only is not None:
        schema_artifact["writeOnly"] = write_only

    return types.SimplePropertyArtifacts(
        type=helpers.property_.type_.Type.SIMPLE,
        description=description,
        schema=schema_artifact,
        required=required,
        open_api=types.OpenApiSimplePropertyArtifacts(
            type=type_,
            format=format_,
            max_length=max_length,
            nullable=nullable,
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
            dict_ignore=dict_ignore,
        ),
    )
