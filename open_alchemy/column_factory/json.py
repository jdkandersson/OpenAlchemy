"""Construct column for json property."""

from .. import types as oa_types
from ..facades.sqlalchemy import json
from . import types


def handle(*, artifacts: oa_types.JsonPropertyArtifacts) -> types.TColumn:
    """
    Handle a json property.

    Args:
        artifacts: The artifacts of the json property.

    Returns:
        The constructed column.

    """
    return json.construct(artifacts=artifacts)
