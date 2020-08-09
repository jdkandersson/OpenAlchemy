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


class _TResultBase(types.TypedDict, total=False):
    """TResult base class for keys that might not be present."""

    reason: str


class TResult(_TResultBase, total=True):
    """Record the result of validation."""

    valid: bool


def t_result_from_result(result: Result) -> TResult:
    """Construct a result dictionary from a result."""
    return_dict: "TResult" = {"valid": result.valid}
    if result.reason is not None:
        return_dict["reason"] = result.reason

    return return_dict


class TProperty(types.TypedDict, total=True):
    """Record validation result of a property."""

    result: TResult


TProperties = typing.Dict[str, TProperty]


class _TModelBase(types.TypedDict, total=False):
    """TModel base class for keys that might not be present."""

    properties: TProperties


class TModel(_TModelBase, total=True):
    """Record validation result of a model."""

    result: TResult


TModels = typing.Dict[str, TModel]


class _TSpecBase(types.TypedDict, total=False):
    """TSpec base class for keys that might not be presents."""

    models: TModels


class TSpec(_TSpecBase, total=True):
    """Record validation result for a specification."""

    result: TResult
