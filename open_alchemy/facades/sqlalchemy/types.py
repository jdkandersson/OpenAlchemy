"""SQLAlchemy types."""

import sqlalchemy
from sqlalchemy import orm

from ... import types as oa_types

# Remapping SQLAlchemy classes
Column = sqlalchemy.Column
Type = sqlalchemy.sql.type_api.TypeEngine
ForeignKey = sqlalchemy.ForeignKey
Integer = sqlalchemy.Integer
BigInteger = sqlalchemy.BigInteger
Number = sqlalchemy.Float
String = sqlalchemy.String
Binary = sqlalchemy.LargeBinary
Date = sqlalchemy.Date
DateTime = sqlalchemy.DateTime
Boolean = sqlalchemy.Boolean
JSON = sqlalchemy.JSON
Relationship = orm.RelationshipProperty


class TOptColumnArgs(oa_types.TypedDict, total=False):
    """Keyword arguments for Column."""

    primary_key: bool
    autoincrement: bool
    index: bool
    unique: bool
