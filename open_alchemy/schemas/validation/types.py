"""Types for validation."""

import typing

from ... import types


class Result(typing.NamedTuple):
    """Result of checking a schema."""

    # Whether the schema is valid
    valid: bool
    # If not valid, the reason why it isn't
    reason: typing.Optional[str]


OptResult = typing.Optional[Result]


class _TModelBase(types.TypedDict, total=False):
    """TModel base class for keys that might not be present."""

    properties: typing.Dict[str, Result]


class TModel(_TModelBase, total=True):
    """Record validation result of a model."""

    result: Result


class _TSpecBase(types.TypedDict, total=False):
    """TSpec base class for keys that might not be presents."""

    models: typing.Dict[str, TModel]


class TSpec(_TSpecBase, total=True):
    """Record validation result for a specification."""

    result: Result
