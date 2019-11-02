"""Types shared across modules."""

import typing

import typing_extensions

Schema = typing.Dict[str, typing.Any]
Schemas = typing.Dict[str, Schema]


class ModelFactory(typing_extensions.Protocol):
    """Defines interface for model factory."""

    def __call__(self, *, name: str) -> typing.Type:
        """Call signature for ModelFactory."""
        ...
