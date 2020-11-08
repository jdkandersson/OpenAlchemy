"""Construct column for relationship property."""

from open_alchemy import facades
from open_alchemy.schemas.artifacts import types as artifact_types


def handle(
    *, artifacts: artifact_types.TAnyRelationshipPropertyArtifacts
) -> facades.sqlalchemy.types.Relationship:
    """
    Handle a relationship property.

    Args:
        artifacts: The artifacts of the relationship property.

    Returns:
        The constructed column.

    """
    return facades.sqlalchemy.relationship.construct(artifacts=artifacts)
