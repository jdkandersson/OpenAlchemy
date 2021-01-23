"""Construct column for simple property."""

from .. import types as oa_types
from ..facades.sqlalchemy import simple
from . import types


def handle(*, artifacts: oa_types.SimplePropertyArtifacts) -> types.TColumn:
    """
    Handle a simple property.

    Args:
        artifacts: The artifacts of the simple property.

    Returns:
        The constructed column.

    """
    return simple.construct(artifacts=artifacts)
