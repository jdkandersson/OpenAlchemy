"""Functions for interacting with the OpenAlchemy models."""

import typing

import sqlalchemy

import open_alchemy

from ..utility_base import TUtilityBase


def get_base() -> typing.Any:
    """
    Get the models.Base used as the declarative base for models.

    Returns:
        The models.Base.

    """
    # pylint: disable=no-member
    return open_alchemy.models.Base  # type: ignore


def set_association(*, table: sqlalchemy.Table, name: str) -> None:
    """
    Set an association table on the models.

    Args:
        table: The association table.
        name: The attribute name to use.

    """
    setattr(open_alchemy.models, name, table)


def get_model(*, name: str) -> typing.Optional[typing.Type[TUtilityBase]]:
    """
    Get a model by name from models.

    Args:
        name: The name of the model.

    Returns:
        The model with the name.

    """
    return getattr(open_alchemy.models, name, None)


def set_model(*, name: str, model: TUtilityBase) -> None:
    """
    Set model by name on models.

    Args:
        model: The model to set.
        name: The name of the model.

    """
    setattr(open_alchemy.models, name, model)
