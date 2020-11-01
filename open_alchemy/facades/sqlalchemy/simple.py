"""SQLAlchemy simple column generation."""

import typing

from open_alchemy.schemas.artifacts import types as artifacts_types

from ... import exceptions
from ... import helpers
from ... import types as oa_types
from . import types


class _TOptColumnArgs(oa_types.TypedDict, total=False):
    """Keyword arguments for Column."""

    primary_key: bool
    autoincrement: bool
    index: bool
    unique: bool


def construct(*, artifacts: artifacts_types.SimplePropertyArtifacts) -> types.Column:
    """
    Construct column from artifacts.

    Args:
        artifacts: The artifacts of the column.

    Returns:
        The SQLAlchemy column.

    """
    type_ = _determine_type(artifacts=artifacts)
    foreign_key: typing.Optional[types.ForeignKey] = None
    if artifacts.extension.foreign_key is not None:
        foreign_key_kwargs: oa_types.TKwargs = {}
        if artifacts.extension.foreign_key_kwargs is not None:
            foreign_key_kwargs = artifacts.extension.foreign_key_kwargs
        foreign_key = types.ForeignKey(
            artifacts.extension.foreign_key, **foreign_key_kwargs
        )
    # Map default value
    default = None
    if artifacts.open_api.default is not None:
        default = helpers.oa_to_py_type.convert(
            value=artifacts.open_api.default,
            type_=artifacts.open_api.type,
            format_=artifacts.open_api.format,
        )

    # Calculate nullable
    nullable = helpers.calculate_nullable(
        nullable=artifacts.open_api.nullable,
        generated=artifacts.extension.autoincrement is True,
        defaulted=default is not None,
        required=artifacts.required,
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
    kwargs: oa_types.TKwargs = {}
    if artifacts.extension.kwargs is not None:
        kwargs = artifacts.extension.kwargs
    return types.Column(
        type_,
        foreign_key,
        nullable=nullable,
        default=default,
        **opt_kwargs,
        **kwargs,
    )


def _determine_type(
    *, artifacts: artifacts_types.SimplePropertyArtifacts
) -> types.Type:
    """
    Determine the type for a specification.

    Raise FeatureNotImplementedError for unsupported types.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The type for the column.

    """
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
    *, artifacts: artifacts_types.SimplePropertyArtifacts
) -> typing.Union[types.Integer, types.BigInteger]:
    """
    Handle artifacts for an integer type.

    Raise FeatureNotImplementedError if a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy integer type of the column.

    """
    if artifacts.open_api.format is None or artifacts.open_api.format == "int32":
        return types.Integer()
    if artifacts.open_api.format == "int64":
        return types.BigInteger()
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.open_api.format} format for integer is not supported."
    )


def _handle_number(
    *, artifacts: artifacts_types.SimplePropertyArtifacts
) -> types.Number:
    """
    Handle artifacts for an number type.

    Raise FeatureNotImplementedError if a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy number type of the column.

    """
    if artifacts.open_api.format is None or artifacts.open_api.format == "float":
        return types.Number()
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.open_api.format} format for number is not supported."
    )


def _handle_string(
    *, artifacts: artifacts_types.SimplePropertyArtifacts
) -> typing.Union[types.String, types.Binary, types.Date, types.DateTime]:
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
            return types.Binary()
        return types.Binary(length=artifacts.open_api.max_length)
    if artifacts.open_api.format == "date":
        return types.Date()
    if artifacts.open_api.format == "date-time":
        return types.DateTime()
    if artifacts.open_api.max_length is None:
        return types.String()
    return types.String(length=artifacts.open_api.max_length)


def _handle_boolean(
    *,
    artifacts: artifacts_types.SimplePropertyArtifacts,  # pylint: disable=unused-argument
) -> types.Boolean:
    """
    Handle artifacts for an boolean type.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy boolean type of the column.

    """
    return types.Boolean()
