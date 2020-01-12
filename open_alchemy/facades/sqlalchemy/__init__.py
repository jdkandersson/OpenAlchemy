"""Facade for SQLAlchemy."""
# pylint: disable=useless-import-alias

import sqlalchemy
from sqlalchemy import orm

from open_alchemy import types

from . import column as column

# Mapping from SQLAlchemy
Column: sqlalchemy.Column = sqlalchemy.Column
Table: sqlalchemy.Table = sqlalchemy.Table


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

    # Construct relationship
    return orm.relationship(
        artifacts.model_name, backref=backref, secondary=artifacts.secondary
    )
