"""Pre-processor that defines any foreign keys."""

from .. import exceptions
from .. import helpers as oa_helpers
from .. import types
from . import helpers
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
    relationship_type = oa_helpers.relationship.calculate_type(
        schema=schema, schemas=schemas
    )
    if relationship_type == oa_helpers.relationship.Type.MANY_TO_MANY:
        return False
    return True


def _foreign_key_property_not_defined(
    schemas: types.Schema,
    parent_schema: types.Schema,
    property_name: str,
    property_schema: types.Schema,
) -> bool:
    """
    Check whether the foreign key property is not already defined.

    Raise MalformedSchemaError if the full relationship schema is not valid.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        parent_schema: The schema that contains the relationship property.
        property_name: The name of the property.
        property_schema: The schema of the property.

    Returns:
        Whether the foreign key property is not already defined.

    """
    full_result = property_.relationship.full.check(
        schemas, parent_schema, property_name, property_schema
    )
    if not full_result.valid:
        raise exceptions.MalformedSchemaError(full_result.reason)

    # Retrieve the property name
    type_ = oa_helpers.relationship.calculate_type(
        schema=property_schema, schemas=schemas
    )
    column_name = oa_helpers.foreign_key.calculate_column_name(
        type_=type_, property_schema=property_schema, schemas=schemas,
    )
    target_schema = oa_helpers.foreign_key.get_target_schema(
        type_=type_,
        parent_schema=parent_schema,
        property_schema=property_schema,
        schemas=schemas,
    )
    foreign_key_property_name = oa_helpers.foreign_key.calculate_prop_name(
        type_=type_,
        column_name=column_name,
        property_name=property_name,
        target_schema=target_schema,
        schemas=schemas,
    )

    # Look for the foreign key property name on the schema the foreign key needs to be
    # defined on
    modify_schema = oa_helpers.foreign_key.get_modify_schema(
        type_=type_,
        parent_schema=parent_schema,
        property_schema=property_schema,
        schemas=schemas,
    )
    properties = helpers.iterate.property_items(schema=modify_schema, schemas=schemas)
    property_names = map(lambda arg: arg[0], properties)
    contains_foreign_key_property_name = any(
        filter(lambda name: name == foreign_key_property_name, property_names)
    )
    if contains_foreign_key_property_name:
        return False
    return True
