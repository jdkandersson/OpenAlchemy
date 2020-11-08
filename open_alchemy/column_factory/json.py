"""Construct column for json property."""

from open_alchemy import facades
from open_alchemy.schemas.artifacts import types as artifact_types


def handle(
    *, artifacts: artifact_types.JsonPropertyArtifacts
) -> facades.sqlalchemy.types.Column:
    """
    Handle a json property.

    Args:
        artifacts: The artifacts of the json property.

    Returns:
        The constructed column.

    """
    return facades.sqlalchemy.json.construct(artifacts=artifacts)
