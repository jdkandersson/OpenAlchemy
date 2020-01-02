"""Column factory functions relating to columns."""

import typing

import sqlalchemy

from open_alchemy import exceptions
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
    column = construct_column(artifacts=artifacts)
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


def construct_column(*, artifacts: types.ColumnArtifacts) -> sqlalchemy.Column:
    """
    Construct column from artifacts.

    Args:
        artifacts: The artifacts of the column.

    Returns:
        The SQLAlchemy column.

    """
    type_ = _determine_type(artifacts=artifacts)
    foreign_key: typing.Optional[sqlalchemy.ForeignKey] = None
    if artifacts.foreign_key is not None:
        foreign_key = sqlalchemy.ForeignKey(artifacts.foreign_key)
    return sqlalchemy.Column(
        type_,
        foreign_key,
        nullable=artifacts.nullable,
        primary_key=artifacts.primary_key,
        autoincrement=artifacts.autoincrement,
        index=artifacts.index,
        unique=artifacts.unique,
    )


def _determine_type(
    *, artifacts: types.ColumnArtifacts
) -> sqlalchemy.sql.type_api.TypeEngine:
    """
    Determine the type for a specification.

    Raise FeatureNotImplementedError for unsupported types.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The type for the column.

    """
    # Determining the type
    type_: typing.Optional[sqlalchemy.sql.type_api.TypeEngine] = None
    if artifacts.type == "integer":
        type_ = _handle_integer(artifacts=artifacts)
    elif artifacts.type == "number":
        type_ = _handle_number(artifacts=artifacts)
    elif artifacts.type == "string":
        type_ = _handle_string(artifacts=artifacts)
    elif artifacts.type == "boolean":
        type_ = _handle_boolean(artifacts=artifacts)

    if type_ is None:
        raise exceptions.FeatureNotImplementedError(
            f"{artifacts.type} has not been implemented"
        )

    return type_


def _handle_integer(
    *, artifacts: types.ColumnArtifacts
) -> typing.Union[sqlalchemy.Integer, sqlalchemy.BigInteger]:
    """
    Handle artifacts for an integer type.

    Raises MalformedSchemaError if max length is defined.
    Raise FeatureNotImplementedError is a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy integer type of the column.

    """
    if artifacts.max_length is not None:
        raise exceptions.MalformedSchemaError(
            "The integer type does not support a maximum length."
        )
    if artifacts.format is None or artifacts.format == "int32":
        return sqlalchemy.Integer
    if artifacts.format == "int64":
        return sqlalchemy.BigInteger
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.format} format for integer is not supported."
    )


def _handle_number(*, artifacts: types.ColumnArtifacts) -> sqlalchemy.Float:
    """
    Handle artifacts for an number type.

    Raises MalformedSchemaError if max length or autoincrement is defined.
    Raise FeatureNotImplementedError is a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy number type of the column.

    """
    if artifacts.max_length is not None:
        raise exceptions.MalformedSchemaError(
            "The number type does not support a maximum length."
        )
    if artifacts.autoincrement is not None:
        raise exceptions.MalformedSchemaError(
            "The number type does not support autoincrement."
        )
    if artifacts.format is None or artifacts.format == "float":
        return sqlalchemy.Float
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.format} format for number is not supported."
    )


def _handle_string(*, artifacts: types.ColumnArtifacts) -> sqlalchemy.String:
    """
    Handle artifacts for an string type.

    Raises MalformedSchemaError if autoincrement is defined.
    Raise FeatureNotImplementedError is a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy string type of the column.

    """
    if artifacts.autoincrement is not None:
        raise exceptions.MalformedSchemaError(
            "The string type does not support autoincrement."
        )
    if artifacts.format in {None, "byte", "password"}:
        if artifacts.max_length is None:
            return sqlalchemy.String
        return sqlalchemy.String(length=artifacts.max_length)
    if artifacts.format == "binary":
        if artifacts.max_length is None:
            return sqlalchemy.LargeBinary
        return sqlalchemy.LargeBinary(length=artifacts.max_length)
    if artifacts.format == "date":
        return sqlalchemy.Date
    if artifacts.format == "date-time":
        return sqlalchemy.DateTime
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.format} format for string is not supported."
    )


def _handle_boolean(*, artifacts: types.ColumnArtifacts) -> sqlalchemy.Boolean:
    """
    Handle artifacts for an boolean type.

    Raises MalformedSchemaError if format, autoincrement or max length is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy boolean type of the column.

    """
    if artifacts.format is not None:
        raise exceptions.MalformedSchemaError(
            "The boolean type does not support format."
        )
    if artifacts.autoincrement is not None:
        raise exceptions.MalformedSchemaError(
            "The boolean type does not support autoincrement."
        )
    if artifacts.max_length is not None:
        raise exceptions.MalformedSchemaError(
            "The boolean type does not support a maximum length."
        )
    return sqlalchemy.Boolean
