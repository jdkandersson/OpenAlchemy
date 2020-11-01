"""SQLAlchemy types."""

import sqlalchemy

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
