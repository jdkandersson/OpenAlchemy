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
        schema: The schema for the column.
        artifacts: The artifacts for the column.
        model_schema: The schema of the model.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name, the SQLAlchemy column based on the schema and the
        specification to store for the column.

    """
    if artifacts.type == oa_types.PropertyType.SIMPLE:
        return simple.handle(artifacts=artifacts)
    if artifacts.type == oa_types.PropertyType.JSON:
        return json.handle(artifacts=artifacts)
    if artifacts.type == oa_types.PropertyType.BACKREF:
        return None
    return relationship.handle(artifacts=artifacts)
