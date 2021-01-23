"""Retrieve artifacts for a simple property."""

from .... import types as oa_types
from ....helpers import peek
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
    type_ = peek.type_(schema=schema, schemas=schemas)
    format_ = peek.prefer_local(get_value=peek.format_, schema=schema, schemas=schemas)
    max_length = peek.prefer_local(
        get_value=peek.max_length, schema=schema, schemas=schemas
    )
    nullable = peek.prefer_local(
        get_value=peek.nullable, schema=schema, schemas=schemas
    )

    description = peek.prefer_local(
        get_value=peek.description, schema=schema, schemas=schemas
    )

    default = peek.prefer_local(get_value=peek.default, schema=schema, schemas=schemas)
    server_default = peek.prefer_local(
        get_value=peek.server_default, schema=schema, schemas=schemas
    )

    read_only = peek.prefer_local(
        get_value=peek.read_only, schema=schema, schemas=schemas
    )
    write_only = peek.prefer_local(
        get_value=peek.write_only, schema=schema, schemas=schemas
    )

    primary_key = peek.prefer_local(
        get_value=peek.primary_key, schema=schema, schemas=schemas
    )
    autoincrement = peek.prefer_local(
        get_value=peek.autoincrement, schema=schema, schemas=schemas
    )
    index = peek.prefer_local(get_value=peek.index, schema=schema, schemas=schemas)
    unique = peek.prefer_local(get_value=peek.unique, schema=schema, schemas=schemas)

    foreign_key = peek.prefer_local(
        get_value=peek.foreign_key, schema=schema, schemas=schemas
    )

    kwargs = peek.prefer_local(get_value=peek.kwargs, schema=schema, schemas=schemas)
    foreign_key_kwargs = peek.prefer_local(
        get_value=peek.foreign_key_kwargs, schema=schema, schemas=schemas
    )

    dict_ignore = peek.dict_ignore(schema=schema, schemas=schemas)

    # Generate the schema
    schema_artifact: oa_types.ColumnSchema = {
        oa_types.OpenApiProperties.TYPE.value: type_
    }
    if format_ is not None:
        schema_artifact[oa_types.OpenApiProperties.FORMAT.value] = format_
    if max_length is not None:
        schema_artifact[oa_types.OpenApiProperties.MAX_LENGTH.value] = max_length
    if description is not None:
        schema_artifact[oa_types.OpenApiProperties.DESCRIPTION.value] = description
    if nullable is not None:
        schema_artifact[oa_types.OpenApiProperties.NULLABLE.value] = nullable
    if default is not None:
        schema_artifact[oa_types.OpenApiProperties.DEFAULT.value] = default
    if read_only is not None:
        schema_artifact[oa_types.OpenApiProperties.READ_ONLY.value] = read_only
    if write_only is not None:
        schema_artifact[oa_types.OpenApiProperties.WRITE_ONLY.value] = write_only
    if dict_ignore is not None:
        schema_artifact[oa_types.ExtensionProperties.DICT_IGNORE.value] = dict_ignore

    return types.SimplePropertyArtifacts(
        type=oa_types.PropertyType.SIMPLE,
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
            primary_key=primary_key is True,
            autoincrement=autoincrement,
            index=index,
            unique=unique,
            server_default=server_default,
            foreign_key=foreign_key,
            kwargs=kwargs,
            foreign_key_kwargs=foreign_key_kwargs,
            dict_ignore=dict_ignore,
        ),
    )
