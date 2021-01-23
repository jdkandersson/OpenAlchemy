"""Types for column factory."""

import typing

from open_alchemy.facades import sqlalchemy

TColumn = sqlalchemy.types.Column
TRelationship = sqlalchemy.types.Relationship
TReturnValue = typing.Optional[typing.Union[TColumn, TRelationship]]
