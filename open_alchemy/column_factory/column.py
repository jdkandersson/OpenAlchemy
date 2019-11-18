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
    kwargs["nullable"] = _calculate_nullable(spec=spec, required=required)
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


def _calculate_nullable(*, spec: types.Schema, required: typing.Optional[bool]) -> bool:
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
        spec: The schema for the column.
        required: Whether the property is required.

    Returns:
        The nullable value for the column.

    """
    nullable = spec.get("nullable")
    if nullable is None:
        if required:
            return False
        return True
    if nullable:
        return True
    return False


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
        type_ = _handle_integer(spec=spec)
    elif spec_type == "number":
        type_ = _handle_number(spec=spec)
    elif spec_type == "string":
        type_ = _handle_string(spec=spec)
    elif spec_type == "boolean":
        type_ = sqlalchemy.Boolean

    if type_ is None:
        raise exceptions.FeatureNotImplementedError(
            f"{spec['type']} has not been implemented"
        )
    return type_


def _handle_integer(
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


def _handle_number(*, spec: types.Schema) -> sqlalchemy.Float:
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


def _handle_string(*, spec: types.Schema) -> sqlalchemy.String:
    """
    Determine the setup of the string to use for the schema.

    Args:
        spec: The schema for the string column.

    Returns:
        String.

    """
    return sqlalchemy.String(length=spec.get("maxLength"))
