"""Construct column for json property."""

import typing

from open_alchemy import facades
from open_alchemy import types
from open_alchemy.schemas.artifacts import types as artifact_types


def handle(
    *, artifacts: artifact_types.JsonPropertyArtifacts
) -> typing.Tuple[facades.sqlalchemy.types.Column, types.Schema]:
    """
    Handle a json property.

    Args:
        artifacts: The artifacts of the json property.

    Returns:
        The constructed column.

    """
    return facades.sqlalchemy.json.construct(artifacts=artifacts), artifacts.schema
