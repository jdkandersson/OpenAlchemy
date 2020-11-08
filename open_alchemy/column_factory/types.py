"""Types for column factory."""

import typing

from open_alchemy import facades

TColumn = facades.sqlalchemy.types.Column
TRelationship = facades.sqlalchemy.types.Relationship
TReturnValue = typing.Optional[typing.Union[TColumn, TRelationship]]
