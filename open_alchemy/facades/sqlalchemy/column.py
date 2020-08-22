"""SQLAlchemy column generation."""

import typing

import sqlalchemy

from ... import exceptions
from ... import helpers
from ... import types

# Remapping SQLAlchemy classes
Column = sqlalchemy.Column
Type = sqlalchemy.sql.type_api.TypeEngine
ForeignKey = sqlalchemy.ForeignKey
Integer = sqlalchemy.Integer
BigInteger = sqlalchemy.BigInteger
Number = sqlalchemy.Float
String = sqlalchemy.String
Binary = sqlalchemy.LargeBinary
Date = sqlalchemy.Date
DateTime = sqlalchemy.DateTime
Boolean = sqlalchemy.Boolean
JSON = sqlalchemy.JSON


class _TOptColumnArgs(types.TypedDict, total=False):
    """Keyword arguments for Column."""

    primary_key: bool
    autoincrement: bool
    index: bool
    unique: bool


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
        foreign_key_kwargs: types.TKwargs = {}
        if artifacts.extension.foreign_key_kwargs is not None:
            foreign_key_kwargs = artifacts.extension.foreign_key_kwargs
        foreign_key = ForeignKey(artifacts.extension.foreign_key, **foreign_key_kwargs)
    # Map default value
    default = None
    if artifacts.open_api.default is not None:
        default = helpers.oa_to_py_type.convert(
            value=artifacts.open_api.default,
            type_=artifacts.open_api.type,
            format_=artifacts.open_api.format,
        )

    # Generate optional keyword arguments
    opt_kwargs: _TOptColumnArgs = {}
    if artifacts.extension.primary_key is not None:
        opt_kwargs["primary_key"] = artifacts.extension.primary_key
    if artifacts.extension.autoincrement is not None:
        opt_kwargs["autoincrement"] = artifacts.extension.autoincrement
    if artifacts.extension.index is not None:
        opt_kwargs["index"] = artifacts.extension.index
    if artifacts.extension.unique is not None:
        opt_kwargs["unique"] = artifacts.extension.unique
    # Generate kwargs
    kwargs: types.TKwargs = {}
    if artifacts.extension.kwargs is not None:
        kwargs = artifacts.extension.kwargs
    return Column(
        type_,
        foreign_key,
        nullable=artifacts.open_api.nullable,
        default=default,
        **opt_kwargs,
        **kwargs,
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
    # Check for JSON
    if artifacts.extension.json:
        return _handle_json(artifacts=artifacts)
    # Determining the type
    if artifacts.open_api.type == "integer":
        return _handle_integer(artifacts=artifacts)
    if artifacts.open_api.type == "number":
        return _handle_number(artifacts=artifacts)
    if artifacts.open_api.type == "string":
        return _handle_string(artifacts=artifacts)
    if artifacts.open_api.type == "boolean":
        return _handle_boolean(artifacts=artifacts)

    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.open_api.type} has not been implemented"
    )


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
        return Integer()
    if artifacts.open_api.format == "int64":
        return BigInteger()
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
        return Number()
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
    if artifacts.open_api.format == "binary":
        if artifacts.open_api.max_length is None:
            return Binary()
        return Binary(length=artifacts.open_api.max_length)
    if artifacts.open_api.format == "date":
        return Date()
    if artifacts.open_api.format == "date-time":
        return DateTime()
    if artifacts.open_api.max_length is None:
        return String()
    return String(length=artifacts.open_api.max_length)


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
    return Boolean()


def _handle_json(
    *, artifacts: types.ColumnArtifacts  # pylint: disable=unused-argument
) -> JSON:
    """
    Handle artifacts for an json type.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy json type of the column.

    """
    return JSON()
