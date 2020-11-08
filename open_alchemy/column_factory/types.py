"""Types for column factory."""

import typing

from open_alchemy import facades

TReturnValue = typing.Optional[
    typing.Union[facades.sqlalchemy.types.Column, facades.sqlalchemy.types.Relationship]
]
