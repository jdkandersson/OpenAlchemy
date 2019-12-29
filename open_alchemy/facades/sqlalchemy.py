"""Facade for SQLAlchemy."""

from sqlalchemy import orm

from open_alchemy import types


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
