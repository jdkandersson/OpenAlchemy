"""Types for UtilityBase."""

import datetime
import typing

from .. import types as oa_types

# Types for converting to dictionary
TSimpleDict = typing.Union[int, float, str, bool]
TOptSimpleDict = typing.Optional[TSimpleDict]
TObjectDict = typing.Dict[str, typing.Any]
TOptObjectDict = typing.Optional[TObjectDict]
TArrayDict = typing.List[TOptObjectDict]
TOptArrayDict = typing.Optional[TArrayDict]
TComplexDict = typing.Union[TOptObjectDict, TOptArrayDict]
TAnyDict = typing.Union[TComplexDict, TOptSimpleDict]
# Types for converting from a dictionary
TStringCol = typing.Union[str, bytes, datetime.date, datetime.datetime]
TSimpleCol = typing.Union[int, float, TStringCol, bool]
TOptSimpleCol = typing.Optional[TSimpleCol]
TObjectCol = typing.Any  # pylint: disable=invalid-name
TOptObjectCol = typing.Optional[TObjectCol]
TArrayCol = typing.Iterable[TOptObjectCol]
TOptArrayCol = typing.Optional[TArrayCol]
TComplexCol = typing.Union[TOptObjectCol, TOptArrayCol]
TAnyCol = typing.Union[TComplexCol, TSimpleCol]


class TModel(oa_types.Protocol):
    """Defines interface for a model."""

    def to_dict(self) -> TObjectDict:
        """Interface for to_dict."""
        ...
