"""SQLAlchemy column generation."""

import typing

import sqlalchemy

from ... import exceptions
from ... import helpers
from ... import types

# Remapping SQLAlchemy classes
Column: sqlalchemy.Column = sqlalchemy.Column
Type: sqlalchemy.sql.type_api.TypeEngine = sqlalchemy.sql.type_api.TypeEngine
ForeignKey: sqlalchemy.ForeignKey = sqlalchemy.ForeignKey
Integer: sqlalchemy.Integer = sqlalchemy.Integer
BigInteger: sqlalchemy.BigInteger = sqlalchemy.BigInteger
Number: sqlalchemy.Float = sqlalchemy.Float
String: sqlalchemy.String = sqlalchemy.String
Binary: sqlalchemy.LargeBinary = sqlalchemy.LargeBinary
Date: sqlalchemy.Date = sqlalchemy.Date
DateTime: sqlalchemy.DateTime = sqlalchemy.DateTime
Boolean: sqlalchemy.Boolean = sqlalchemy.Boolean


def construct(*, artifacts: types.ColumnArtifacts) -> Column:
    """
    Construct column from artifacts.

    Args:
        artifacts: The artifacts of the column.

    Returns:
        The SQLAlchemy column.

    """
    type_ = _determine_type(artifacts=artifacts)
    foreign_key: typing.Optional[ForeignKey] = None
    if artifacts.extension.foreign_key is not None:
        foreign_key = ForeignKey(artifacts.extension.foreign_key)
    # Map default value
    default = helpers.oa_to_py_type.convert(
        value=artifacts.open_api.default,
        type_=artifacts.open_api.type,
        format_=artifacts.open_api.format,
    )
    return Column(
        type_,
        foreign_key,
        nullable=artifacts.open_api.nullable,
        default=default,
        primary_key=artifacts.extension.primary_key,
        autoincrement=artifacts.extension.autoincrement,
        index=artifacts.extension.index,
        unique=artifacts.extension.unique,
    )


def _determine_type(*, artifacts: types.ColumnArtifacts) -> Type:
    """
    Determine the type for a specification.

    Raise FeatureNotImplementedError for unsupported types.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The type for the column.

    """
    # Determining the type
    type_: typing.Optional[Type] = None
    if artifacts.open_api.type == "integer":
        type_ = _handle_integer(artifacts=artifacts)
    elif artifacts.open_api.type == "number":
        type_ = _handle_number(artifacts=artifacts)
    elif artifacts.open_api.type == "string":
        type_ = _handle_string(artifacts=artifacts)
    elif artifacts.open_api.type == "boolean":
        type_ = _handle_boolean(artifacts=artifacts)

    if type_ is None:
        raise exceptions.FeatureNotImplementedError(
            f"{artifacts.open_api.type} has not been implemented"
        )

    return type_


def _handle_integer(
    *, artifacts: types.ColumnArtifacts
) -> typing.Union[Integer, BigInteger]:
    """
    Handle artifacts for an integer type.

    Raise FeatureNotImplementedError if a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy integer type of the column.

    """
    if artifacts.open_api.format is None or artifacts.open_api.format == "int32":
        return Integer
    if artifacts.open_api.format == "int64":
        return BigInteger
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.open_api.format} format for integer is not supported."
    )


def _handle_number(*, artifacts: types.ColumnArtifacts) -> Number:
    """
    Handle artifacts for an number type.

    Raise FeatureNotImplementedError if a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy number type of the column.

    """
    if artifacts.open_api.format is None or artifacts.open_api.format == "float":
        return Number
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.open_api.format} format for number is not supported."
    )


def _handle_string(
    *, artifacts: types.ColumnArtifacts
) -> typing.Union[String, Binary, Date, DateTime]:
    """
    Handle artifacts for an string type.

    Raise FeatureNotImplementedError if a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy string type of the column.

    """
    if artifacts.open_api.format in {None, "byte", "password"}:
        if artifacts.open_api.max_length is None:
            return String
        return String(length=artifacts.open_api.max_length)
    if artifacts.open_api.format == "binary":
        if artifacts.open_api.max_length is None:
            return Binary
        return Binary(length=artifacts.open_api.max_length)
    if artifacts.open_api.format == "date":
        return Date
    if artifacts.open_api.format == "date-time":
        return DateTime
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.open_api.format} format for string is not supported."
    )


def _handle_boolean(
    *, artifacts: types.ColumnArtifacts  # pylint: disable=unused-argument
) -> Boolean:
    """
    Handle artifacts for an boolean type.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy boolean type of the column.

    """
    return Boolean
