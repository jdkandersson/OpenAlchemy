"""Base class providing utilities for SQLAlchemy models."""

import typing

from . import exceptions
from . import types


class UtilityBase:
    """Base class providing utilities for SQLAlchemy models."""

    _schema: types.Schema

    def to_dict(self) -> typing.Dict:
        """
        Convert model instance to dictionary.

        Raise ModelAttributeError if _schema is not defined.

        Returns:
            The dictionary representation of the model.

        """
        if not hasattr(self, "_schema"):
            raise exceptions.ModelAttributeError(
                "Model does not have a record of its schema."
            )
        return {}
