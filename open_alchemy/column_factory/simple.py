"""Construct column for simple property."""

import typing

from open_alchemy import facades
from open_alchemy import types
from open_alchemy.schemas.artifacts import types as artifact_types


def handle(
    *, artifacts: artifact_types.SimplePropertyArtifacts
) -> typing.Tuple[facades.sqlalchemy.types.Column, types.ColumnSchema]:
    """
    Handle a simple property.

    Args:
        artifacts: The artifacts of the simple property.

    Returns:
        The constructed column.

    """
    return facades.sqlalchemy.simple.construct(artifacts=artifacts), artifacts.schema
