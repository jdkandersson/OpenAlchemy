"""Retrieve artifacts for a simple property."""

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema
) -> types.SimplePropertyArtifacts:
    """
    Retrieve the artifacts for a simple property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the simple property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    format_ = oa_helpers.peek.format_(schema=schema, schemas=schemas)

    return types.SimplePropertyArtifacts(
        property_type=helpers.property_.type_.Type.SIMPLE, type_=type_, format_=format_
    )
