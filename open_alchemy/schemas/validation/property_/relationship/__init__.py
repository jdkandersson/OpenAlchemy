"""Define validation rules for relationship."""


from ..... import types as oa_types
from ... import types
from . import full
from . import property_


def check(
    schemas: oa_types.Schemas,
    parent_schema: oa_types.Schema,
    property_name: str,
    property_schema: oa_types.Schema,
) -> types.Result:
    """
    Check the schema of a relationship.

    Args:
        schemas: All the schemas used to resolve any $ref.
        parent_schema: The schema with the embedded relationship property.
        property_name: The name of the relationship property.
        property_schema: The schema of the relationship property.

    Returns:
        Whether the schema is valid and the reason if it is not.

    """
    # Validate the property schema
    property_result = property_.check(schemas, property_schema)
    if not property_result.valid:
        return property_result

    # Validate the full schema
    return full.check(schemas, parent_schema, property_name, property_schema)
