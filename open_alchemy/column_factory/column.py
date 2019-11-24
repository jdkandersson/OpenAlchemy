"""Column factory functions relating to columns."""

import typing

import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types


def handle_column(
    *, spec: types.Schema, required: typing.Optional[bool] = None
) -> sqlalchemy.Column:
    """
    Generate column based on OpenAPI schema property.

    Assume any $ref and allOf has already been resolved.

    Args:
        spec: The schema for the column.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.

    Returns:
        The logical name and the SQLAlchemy column based on the schema.

    """
    return _spec_to_column(spec=spec, required=required)


def check_schema(
    *, schema: types.Schema, required: typing.Optional[bool] = None
) -> typing.Tuple[types.ColumnSchema, types.ColumnArtifacts]:
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

    # Construct schema to return
    return_schema: types.ColumnSchema = {"type": type_}
    if format_ is not None:
        return_schema["format"] = format_
    if max_length is not None:
        return_schema["maxLength"] = max_length
    if nullable is not None:
        return_schema["nullable"] = nullable

    # Construct return artifacts
    nullable_artefact = _calculate_nullable(nullable=nullable, required=required)
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

    return return_schema, return_artifacts


def _calculate_nullable(
    *, nullable: typing.Optional[bool], required: typing.Optional[bool]
) -> bool:
    """
    Calculate the value of the nullable field.

    The following is the truth table for the nullable property.
    required  | schema nullable | returned nullable
    --------------------------------------------------------
    None      | not given       | True
    None      | False           | False
    None      | True            | True
    False     | not given       | True
    False     | False           | False
    False     | True            | True
    True      | not given       | False
    True      | False           | False
    True      | True            | True

    To summarize, if nullable is the schema the value for it is used. Otherwise True
    is returned unless required is True.

    Args:
        nullable: Whether the property is nullable.
        required: Whether the property is required.

    Returns:
        The nullable value for the column.

    """
    if nullable is None:
        if required:
            return False
        return True
    if nullable:
        return True
    return False


def _spec_to_column(
    *, spec: types.Schema, required: typing.Optional[bool] = None
) -> sqlalchemy.Column:
    """
    Convert specification to a SQLAlchemy column.

    Args:
        spec: The schema for the column.
        required: Whether the object property is required.

    Returns:
        The SQLAlchemy column based on the schema.

    """
    # Keep track of column arguments
    args: typing.Tuple[typing.Any, ...] = ()
    kwargs: types.Schema = {}

    # Calculate column modifiers
    kwargs["nullable"] = _calculate_nullable(
        nullable=spec.get("nullable", None), required=required
    )
    if helpers.get_ext_prop(source=spec, name="x-primary-key"):
        kwargs["primary_key"] = True
    autoincrement = helpers.get_ext_prop(source=spec, name="x-autoincrement")
    if autoincrement is not None:
        if autoincrement:
            kwargs["autoincrement"] = True
        else:
            kwargs["autoincrement"] = False
    if helpers.get_ext_prop(source=spec, name="x-index"):
        kwargs["index"] = True
    if helpers.get_ext_prop(source=spec, name="x-unique"):
        kwargs["unique"] = True
    foreign_key = helpers.get_ext_prop(source=spec, name="x-foreign-key")
    if foreign_key:
        args = (*args, sqlalchemy.ForeignKey(foreign_key))

    # Calculating type of column
    type_ = _determine_type(spec=spec)

    return sqlalchemy.Column(type_, *args, **kwargs)


def _determine_type(*, spec: types.Schema) -> sqlalchemy.sql.type_api.TypeEngine:
    """
    Determine the type for a specification.

    If no type is found, raises TypeMissingError. If the type is found but is not
    handled, raises FeatureNotImplementedError.

    Args:
        spec: The specification to determine the type for.

    Returns:
        The type for the specification.

    """
    # Checking for type
    spec_type = spec.get("type")
    if spec_type is None:
        raise exceptions.TypeMissingError("Every property requires a type.")

    # Determining the type
    type_: typing.Optional[sqlalchemy.sql.type_api.TypeEngine] = None
    if spec_type == "integer":
        type_ = _handle_integer_spec(spec=spec)
    elif spec_type == "number":
        type_ = _handle_number_spec(spec=spec)
    elif spec_type == "string":
        type_ = _handle_string_spec(spec=spec)
    elif spec_type == "boolean":
        type_ = sqlalchemy.Boolean

    if type_ is None:
        raise exceptions.FeatureNotImplementedError(
            f"{spec['type']} has not been implemented"
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


def _handle_integer_spec(
    *, spec: types.Schema
) -> typing.Union[sqlalchemy.Integer, sqlalchemy.BigInteger]:
    """
    Determine the type of integer to use for the schema.

    Args:
        spec: The schema for the integer column.

    Returns:
        Integer or BigInteger depending on the format.

    """
    if spec.get("format", "int32") == "int32":
        return sqlalchemy.Integer
    if spec.get("format") == "int64":
        return sqlalchemy.BigInteger
    raise exceptions.FeatureNotImplementedError(
        f"{spec.get('format')} format for integer is not supported."
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
            "The number type does not support a autoincrement."
        )
    if artifacts.format is None or artifacts.format == "float":
        return sqlalchemy.Float
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.format} format for number is not supported."
    )


def _handle_number_spec(*, spec: types.Schema) -> sqlalchemy.Float:
    """
    Determine the type of number to use for the schema.

    Args:
        spec: The schema for the number column.

    Returns:
        Float.

    """
    if spec.get("format", "float") == "float":
        return sqlalchemy.Float
    raise exceptions.FeatureNotImplementedError(
        f"{spec.get('format')} format for number is not supported."
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
            "The string type does not support a autoincrement."
        )
    if artifacts.format is None:
        return sqlalchemy.String(length=artifacts.max_length)
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.format} format for string is not supported."
    )


def _handle_string_spec(*, spec: types.Schema) -> sqlalchemy.String:
    """
    Determine the setup of the string to use for the schema.

    Args:
        spec: The schema for the string column.

    Returns:
        String.

    """
    return sqlalchemy.String(length=spec.get("maxLength"))
