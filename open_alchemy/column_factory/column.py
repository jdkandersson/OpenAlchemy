"""Column factory functions relating to columns."""

import typing

import sqlalchemy

from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy import types


def handle_column(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    required: typing.Optional[bool] = None,
) -> sqlalchemy.Column:
    """
    Generate column based on OpenAPI schema property.

    Assume any $ref and allOf has already been resolved.

    Args:
        schema: The schema for the column.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.

    Returns:
        The logical name and the SQLAlchemy column based on the schema.

    """
    schema = helpers.prepare_schema(schema=schema, schemas=schemas)
    artifacts = check_schema(schema=schema, required=required)
    column_schema = _calculate_column_schema(artifacts=artifacts, schema=schema)
    column = facades.sqlalchemy.column.construct(artifacts=artifacts)
    return column_schema, column


def check_schema(
    *, schema: types.Schema, required: typing.Optional[bool] = None
) -> types.ColumnArtifacts:
    """
    Check schema and transform into consistent schema and get the column artifacts.

    Raise TypeMissingError of the type is not in the schema or is not a string.
    Raise MalformedSchemaError if format, maxLength or nullable are not of the correct
    type.
    Raise MalformedExtensionPropertyError if an extension property is of the wrong
    type.

    Args:
        schema: The schema to check.

    Returns:
        The schema against which to check dictionaries and the artifacts required to
        construct the column as a tuple.

    """
    # Retrieve artifacts
    type_ = helpers.peek.type_(schema=schema, schemas={})
    format_ = helpers.peek.format_(schema=schema, schemas={})
    max_length = helpers.peek.max_length(schema=schema, schemas={})
    nullable = helpers.peek.nullable(schema=schema, schemas={})
    primary_key = helpers.get_ext_prop(source=schema, name="x-primary-key")
    autoincrement = helpers.get_ext_prop(source=schema, name="x-autoincrement")
    index = helpers.get_ext_prop(source=schema, name="x-index")
    unique = helpers.get_ext_prop(source=schema, name="x-unique")
    foreign_key = helpers.get_ext_prop(source=schema, name="x-foreign-key")

    # Construct return artifacts
    nullable_artefact = helpers.calculate_nullable(
        nullable=nullable, generated=autoincrement is True, required=required
    )
    return_artifacts = types.ColumnArtifacts(
        type_,
        format=format_,
        max_length=max_length,
        nullable=nullable_artefact,
        primary_key=primary_key,
        autoincrement=autoincrement,
        index=index,
        unique=unique,
        foreign_key=foreign_key,
    )

    return return_artifacts


def calculate_schema(
    *,
    artifacts: types.ColumnArtifacts,
    nullable: typing.Optional[bool] = None,
    dict_ignore: typing.Optional[bool] = None,
) -> types.ColumnSchema:
    """
    Calculate the schema to return based on column artifacts.

    Args:
        artifacts: The artifacts for the column construction.

    Returns:
        The schema to be recorded for the column.

    """
    schema: types.ColumnSchema = {"type": artifacts.type}
    if artifacts.format is not None:
        schema["format"] = artifacts.format
    if artifacts.max_length is not None:
        schema["maxLength"] = artifacts.max_length
    if artifacts.autoincrement is not None:
        schema["x-generated"] = artifacts.autoincrement
    if dict_ignore is not None:
        schema["x-dict-ignore"] = dict_ignore
    if nullable is not None:
        schema["nullable"] = nullable
    return schema


def _calculate_column_schema(
    *, artifacts: types.ColumnArtifacts, schema: types.Schema
) -> types.ColumnSchema:
    """
    Calculate the schema to be returned for a column.

    Similar to calculate_schema with the addition of checking the schema for
    x-dict-ignore.

    Assume that any $ref and allOf for the schema has already been resolved.

    Args:
        artifacts: The artifacts for the column construction.
        schema: The schema for the column.

    Returns:
        The schema to be recorded for the column.

    """
    nullable = helpers.peek.nullable(schema=schema, schemas={})
    dict_ignore = helpers.get_ext_prop(source=schema, name="x-dict-ignore")
    return_schema = calculate_schema(
        artifacts=artifacts, nullable=nullable, dict_ignore=dict_ignore
    )
    return return_schema
