"""Types for UtilityBase."""

import typing

from .. import types as oa_types

TSimpleDict = typing.Union[int, float, str, bool]
TOptSimpleDict = typing.Optional[TSimpleDict]
TObjectDict = typing.Dict[str, typing.Any]
TOptObjectDict = typing.Optional[TObjectDict]
TArrayDict = typing.List[TOptObjectDict]
TOptArrayDict = typing.Optional[TArrayDict]
TComplexDict = typing.Union[TOptObjectDict, TOptArrayDict]
TAny = typing.Union[TComplexDict, TOptSimpleDict]


class TModel(oa_types.Protocol):
    """Defines interface for a model."""

    def to_dict(self) -> TObjectDict:
        """Interface for to_dict."""
        ...
