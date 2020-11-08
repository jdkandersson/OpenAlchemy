"""Construct column for json property."""

from .. import facades
from .. import types as oa_types
from . import types


def handle(*, artifacts: oa_types.JsonPropertyArtifacts) -> types.TColumn:
    """
    Handle a json property.

    Args:
        artifacts: The artifacts of the json property.

    Returns:
        The constructed column.

    """
    return facades.sqlalchemy.json.construct(artifacts=artifacts)
