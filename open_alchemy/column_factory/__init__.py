"""Generate columns based on OpenAPI schema property."""

from open_alchemy import types as oa_types

from . import json
from . import relationship
from . import simple
from . import types


def column_factory(*, artifacts: oa_types.TAnyPropertyArtifacts) -> types.TReturnValue:
    """
    Generate column based on OpenAPI schema property.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The column, relationship or None if the property does not need it.

    """
    if artifacts.type == oa_types.PropertyType.SIMPLE:
        return simple.handle(artifacts=artifacts)
    if artifacts.type == oa_types.PropertyType.JSON:
        return json.handle(artifacts=artifacts)
    if artifacts.type == oa_types.PropertyType.BACKREF:
        return None
    return relationship.handle(artifacts=artifacts)
