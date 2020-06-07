"""Facade for SQLAlchemy."""
# pylint: disable=useless-import-alias

import typing

import sqlalchemy
from sqlalchemy import orm

from open_alchemy import types

from . import column as column

# Mapping from SQLAlchemy
Table = sqlalchemy.Table
Relationship = orm.RelationshipProperty


def relationship(*, artifacts: types.RelationshipArtifacts) -> orm.RelationshipProperty:
    """
    Construct relationship.

    Args:
        artifacts: Information for the relationship to construct.

    Returns:
        The constructed relationship.

    """
    # Construct back reference
    backref = None
    if artifacts.back_reference is not None:
        backref = orm.backref(
            artifacts.back_reference.property_name,
            uselist=artifacts.back_reference.uselist,
        )

    # Construct kwargs
    kwargs: typing.Dict[str, typing.Any] = {}
    if artifacts.kwargs is not None:
        kwargs = artifacts.kwargs

    # Construct relationship
    return orm.relationship(
        artifacts.model_name, backref=backref, secondary=artifacts.secondary, **kwargs
    )


def table(
    *, tablename: str, base: typing.Any, columns: typing.Tuple[column.Column, ...]
) -> Table:
    """
    Construct table.

    Args:
        tablename: The name of the table to construct.
        base: The base class for the table containing metadata.
        columns: The columns of the table.

    Returns:
        The SQLAlchemy table.

    """
    return Table(tablename, base.metadata, *columns)
