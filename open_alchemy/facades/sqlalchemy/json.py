"""SQLAlchemy json column generation."""

import typing

from ... import types as oa_types
from ...helpers import calculate_nullable
from . import types


def construct(*, artifacts: oa_types.JsonPropertyArtifacts) -> types.Column:
    """
    Construct column from artifacts.

    Args:
        artifacts: The artifacts of the column.

    Returns:
        The SQLAlchemy column.

    """
    type_ = types.JSON()
    foreign_key: typing.Optional[types.ForeignKey] = None
    if artifacts.extension.foreign_key is not None:
        foreign_key_kwargs: oa_types.TKwargs = {}
        if artifacts.extension.foreign_key_kwargs is not None:
            foreign_key_kwargs = artifacts.extension.foreign_key_kwargs
        foreign_key = types.ForeignKey(
            artifacts.extension.foreign_key, **foreign_key_kwargs
        )

    # Calculate nullable
    nullable = calculate_nullable.calculate_nullable(
        nullable=artifacts.open_api.nullable,
        generated=False,
        defaulted=False,
        required=artifacts.required,
    )

    # Generate optional keyword arguments
    opt_kwargs: types.TOptColumnArgs = {}
    if artifacts.extension.primary_key is not None:
        opt_kwargs["primary_key"] = artifacts.extension.primary_key
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
        **opt_kwargs,
        **kwargs,
    )
