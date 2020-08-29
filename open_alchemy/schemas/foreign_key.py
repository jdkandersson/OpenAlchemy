"""Pre-processor that defines any foreign keys."""

import typing

from .. import helpers as oa_helpers
from .. import types
from . import helpers


def _requires_foreign_key(schemas: types.Schemas, schema: types.Schema) -> bool:
    """
    Check whether the property requires a foreign key to be defined.

    Assume schema is valid.

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
    # Filter for relationship properties
    property_type = helpers.property_.type_.calculate(schemas, schema)
    if property_type != helpers.property_.type_.Type.RELATIONSHIP:
        return False

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

    Assume the full relationship schema is valid.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        parent_schema: The schema that contains the relationship property.
        property_name: The name of the property.
        property_schema: The schema of the property.

    Returns:
        Whether the foreign key property is not already defined.

    """
    # Retrieve the property name
    type_ = oa_helpers.relationship.calculate_type(
        schema=property_schema, schemas=schemas
    )
    column_name = oa_helpers.foreign_key.calculate_column_name(
        type_=type_,
        property_schema=property_schema,
        schemas=schemas,
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
    properties = helpers.iterate.properties_items(schema=modify_schema, schemas=schemas)
    property_names = map(lambda arg: arg[0], properties)
    contains_foreign_key_property_name = any(
        filter(lambda name: name == foreign_key_property_name, property_names)
    )
    if contains_foreign_key_property_name:
        return False
    return True


class TArtifacts(helpers.process.TArtifacts):
    """The return value of _calculate_schema."""

    property_schema: types.ColumnSchema


def _calculate_foreign_key_property_artifacts(
    schemas: types.Schema,
    parent_name: str,
    parent_schema: types.Schema,
    property_name: str,
    property_schema: types.Schema,
) -> TArtifacts:
    """
    Calculate the artifacts for the schema for the foreign key property.

    Assume the full relationship schema is valid.
    Assume that the relationship is not many-to-many

    Args:
        schemas: All defined schemas used to resolve any $ref.
        parent_name: The name of the schema that contains the relationship property.
        parent_schema: The schema that contains the relationship property.
        property_name: The name of the property.
        property_schema: The schema of the property.

    Returns:
        The name of the schema to store the property onto and the name and schema of the
        foreign key property.

    """
    # Retrieve the schema of the property that is targeted by the foreign key
    relationship_type = oa_helpers.relationship.calculate_type(
        schema=property_schema, schemas=schemas
    )
    assert relationship_type != oa_helpers.relationship.Type.MANY_TO_MANY

    column_name = oa_helpers.foreign_key.calculate_column_name(
        type_=relationship_type,
        property_schema=property_schema,
        schemas=schemas,
    )
    target_schema = oa_helpers.foreign_key.get_target_schema(
        type_=relationship_type,
        parent_schema=parent_schema,
        property_schema=property_schema,
        schemas=schemas,
    )
    target_schema_properties = helpers.iterate.properties_items(
        schema=target_schema, schemas=schemas
    )
    foreign_key_target = next(
        filter(lambda arg: arg[0] == column_name, target_schema_properties), None
    )
    assert foreign_key_target is not None
    _, foreign_key_target_schema = foreign_key_target

    # Check whether the property is required
    required: typing.Optional[bool] = None
    if relationship_type != oa_helpers.relationship.Type.ONE_TO_MANY:
        required_items = helpers.iterate.required_items(
            schema=parent_schema, schemas=schemas
        )
        required = any(filter(lambda name: name == property_name, required_items))
    # Calculate nullable for all but one-to-many relationships based on property
    nullable: typing.Optional[bool] = None
    relationship_type = oa_helpers.relationship.calculate_type(
        schema=property_schema, schemas=schemas
    )
    if relationship_type != oa_helpers.relationship.Type.ONE_TO_MANY:
        nullable = oa_helpers.peek.nullable(schema=property_schema, schemas=schemas)
    default = oa_helpers.peek.default(schema=foreign_key_target_schema, schemas=schemas)
    nullable = oa_helpers.calculate_nullable(
        nullable=nullable,
        generated=False,
        defaulted=default is not None,
        required=required,
    )

    # Retrieve information about the foreign key schema
    foreign_key = oa_helpers.foreign_key.calculate_foreign_key(
        column_name=column_name,
        target_schema=target_schema,
        schemas=schemas,
    )
    property_type = oa_helpers.peek.type_(
        schema=foreign_key_target_schema, schemas=schemas
    )
    format_ = oa_helpers.peek.format_(schema=foreign_key_target_schema, schemas=schemas)
    max_length = oa_helpers.peek.max_length(
        schema=foreign_key_target_schema, schemas=schemas
    )

    # Calculate the schema
    foreign_key_property_schema: types.ColumnSchema = {
        "type": property_type,
        "x-dict-ignore": True,
        "nullable": nullable,
        "x-foreign-key": foreign_key,
    }
    if format_ is not None:
        foreign_key_property_schema["format"] = format_
    if max_length is not None:
        foreign_key_property_schema["maxLength"] = max_length
    if default is not None:
        foreign_key_property_schema["default"] = default

    # Calculate other artifacts
    modify_name = oa_helpers.foreign_key.get_modify_name(
        type_=relationship_type,
        parent_name=parent_name,
        property_schema=property_schema,
        schemas=schemas,
    )
    foreign_key_property_name = oa_helpers.foreign_key.calculate_prop_name(
        type_=relationship_type,
        column_name=column_name,
        property_name=property_name,
        target_schema=target_schema,
        schemas=schemas,
    )

    return TArtifacts(
        modify_name, foreign_key_property_name, foreign_key_property_schema
    )


def _get_schema_foreign_keys(
    schemas: types.Schemas,
    schema_name: str,
    schema: types.Schema,
) -> helpers.process.TArtifactsIter:
    """
    Retrieve the foreign keys for a schema.

    Assume schema is constructable.

    Algorithm:
    1. validate property schema and filter for whether a foreign key is required,
    2. validate the full relationship schema and filter for foreign keys not already
        defined and
    3. capture the artifacts for the foreign key.

    Args:
        schemas: All schemas.
        schema_name: The name of the schema.
        schema: A constructable schema.

    Returns:
        Iterable with all foreign keys of the constructable schema.

    """
    # Get all the properties of the schema
    names_properties = helpers.iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    # Validate and remove properties that don't require foreign keys
    foreign_key_name_properties = filter(
        lambda args: _requires_foreign_key(schemas, args[1]), names_properties
    )
    # Validate relationship and remove properties that already have a defined foreign
    # key
    undefined_foreign_key_name_properties = filter(
        lambda args: _foreign_key_property_not_defined(
            schemas, schema, args[0], args[1]
        ),
        foreign_key_name_properties,
    )
    # Convert to artifacts
    return map(
        lambda args: _calculate_foreign_key_property_artifacts(
            schemas, schema_name, schema, args[0], args[1]
        ),
        undefined_foreign_key_name_properties,
    )


def _foreign_keys_to_schema(
    foreign_keys: helpers.process.TArtifactsIter,
) -> types.Schema:
    """
    Convert to the schema with the foreign keys from foreign key artifacts.

    Args:
        foreign_keys: The foreign keys to convert.

    Returns:
        The schema with the foreign keys.

    """
    return {
        "type": "object",
        "properties": {
            property_name: schema for _, property_name, schema in foreign_keys
        },
    }


def process(*, schemas: types.Schemas):
    """
    Pre-process the schemas to add foreign keys as required.

    Args:
        schemas: The schemas to process.

    """
    # Retrieve foreign keys
    foreign_keys = helpers.process.get_artifacts(
        schemas=schemas, get_schema_artifacts=_get_schema_foreign_keys
    )
    # Map to a schema for each grouped foreign keys
    foreign_key_schemas = helpers.process.calculate_outputs(
        artifacts=foreign_keys, calculate_output=_foreign_keys_to_schema
    )
    # Convert to list to resolve iterator
    foreign_key_schema_list = list(foreign_key_schemas)
    # Add foreign keys to schemas
    for name, foreign_key_schema in foreign_key_schema_list:
        schemas[name] = {"allOf": [schemas[name], foreign_key_schema]}
