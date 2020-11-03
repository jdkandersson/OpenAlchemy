"""Construct relationship properties."""

import typing

from sqlalchemy import orm

from open_alchemy import types as oa_types

from . import types


def construct(
    *, artifacts: oa_types.TAnyRelationshipPropertyArtifacts
) -> types.Relationship:
    """
    Construct relationship from artifacts.

    Args:
        artifacts: The artifacts of the relationship.

    Returns:
        The SQLAlchemy relationship.

    """
    # Construct back reference
    backref = None
    if artifacts.backref_property is not None:
        # Calculate uselist
        uselist: typing.Optional[bool] = None
        if artifacts.sub_type == oa_types.RelationshipType.ONE_TO_ONE:
            uselist = False

        backref = orm.backref(
            artifacts.backref_property,
            uselist=uselist,
        )

    # Calculate secondary
    secondary: typing.Optional[str] = None
    if artifacts.sub_type == oa_types.RelationshipType.MANY_TO_MANY:
        secondary = artifacts.secondary

    # Construct kwargs
    kwargs: typing.Dict[str, typing.Any] = {}
    if artifacts.kwargs is not None:
        kwargs = artifacts.kwargs

    # Construct relationship
    return orm.relationship(
        artifacts.parent, backref=backref, secondary=secondary, **kwargs
    )
