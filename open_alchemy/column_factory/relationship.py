"""Construct column for relationship property."""

from .. import types as oa_types
from ..facades.sqlalchemy import relationship
from . import types


def handle(
    *, artifacts: oa_types.TAnyRelationshipPropertyArtifacts
) -> types.TRelationship:
    """
    Handle a relationship property.

    Args:
        artifacts: The artifacts of the relationship property.

    Returns:
        The constructed column.

    """
    return relationship.construct(artifacts=artifacts)
