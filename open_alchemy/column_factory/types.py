"""Types for column factory."""

import typing

from open_alchemy.facades.sqlalchemy import types

TColumn = types.Column
TRelationship = types.Relationship
TReturnValue = typing.Optional[typing.Union[TColumn, TRelationship]]
