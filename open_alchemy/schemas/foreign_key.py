"""Pre-processor that defines any foreign keys."""

from .. import exceptions
from .. import helpers
from .. import types
from .validation import property_


def _requires_foreign_key(schemas: types.Schemas, schema: types.Schema) -> bool:
    """
    Check whether the property requires a foreign key to be defined.

    Raise MalformedSchemaError if the property is not valid.
    Raise MalformedSchemaError if the property is a relationship but it is not valid.

    Foreign keys are required for many-to-one, one-to-one and one-to-many relationships.
    The following rules capture this:
    1. relationship property that is not
    2. a many-to-many relationship.

    Args:
        schemas: All the defined schemas used to resolve any $ref.
        schema: The schema of the property.

    Returns:
        Whether the property requires a foreign key.

    """
    # Check for valid property
    type_result = property_.check_type(schemas, schema)
    if not type_result.valid:
        raise exceptions.MalformedSchemaError(type_result.reason)

    # Filter for relationship properties
    property_type = property_.calculate_type(schemas, schema)
    if property_type != property_.Type.RELATIONSHIP:
        return False

    # Check for valid relationship
    relationship_result = property_.relationship.property_.check(
        schema=schema, schemas=schemas
    )
    if not relationship_result.valid:
        raise exceptions.MalformedSchemaError(relationship_result.reason)

    # Filter for not many-to-many relationship
    relationship_type = helpers.relationship.calculate_type(
        schema=schema, schemas=schemas
    )
    if relationship_type == helpers.relationship.Type.MANY_TO_MANY:
        return False
    return True


# def _foreign_key_defined(
#     schemas: types.Schemas,
#     parent_schema: types.Schema,
#     property_name: str,
#     property_schema: types.Schema,
# ) -> bool:
#     """
#     Check whether a foreign key has already been defined.

#     Assume that the property defines a x-to-one or one-to-many relationship.
#     Assume that the schema has already been verified.

#     Args:
#         schemas: All defined schemas used to resolve any $ref.
#         parent_schema: The schema the property is embedded in.
#         property_name: The name of the property.
#         property_schema: The schema of the propert.

#     Returns:
#         Whether a foreign key has already been defined.

#     """
