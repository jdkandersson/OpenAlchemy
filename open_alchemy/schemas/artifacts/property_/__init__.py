"""Gather artifacts for a property."""

from .... import types as oa_types
from ....helpers import property_
from .. import types
from . import backref
from . import json
from . import relationship
from . import simple


def get(
    schemas: oa_types.Schemas,
    model_schema: oa_types.Schema,
    property_name: str,
    schema: oa_types.Schema,
    required: bool,
) -> types.TAnyPropertyArtifacts:
    """
    Retrieve the artifacts for a property.

    Args:
        schemas: All the defined schemas.
        model_schema: The schema that contains the property.
        property_name: The name of the property.
        schema: The schema of the property to gather artifacts for.
        required: WHether the property appears in the required list.

    Returns:
        The artifacts for the property.

    """
    type_ = property_.calculate_type(schema=schema, schemas=schemas)

    if type_ == oa_types.PropertyType.SIMPLE:
        return simple.get(schemas, schema, required)

    if type_ == oa_types.PropertyType.JSON:
        return json.get(schemas, schema, required)

    if type_ == oa_types.PropertyType.BACKREF:
        return backref.get(schemas, schema)

    assert type_ == oa_types.PropertyType.RELATIONSHIP
    return relationship.get(schemas, model_schema, property_name, schema, required)
