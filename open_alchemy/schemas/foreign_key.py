"""Pre-processor that defines any foreign keys."""

import typing

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


class _ForeignKeyArtifacts(typing.NamedTuple):
    """The return value of _calculate_schema."""

    modify_schema_name: str
    foreign_key_property_name: str
    foreign_key_property_schema: types.ColumnSchema


_ForeignKeyArtifactsIter = typing.Iterable[_ForeignKeyArtifacts]
_ForeignKeyArtifactsGroupedIter = typing.Iterable[
    typing.Tuple[str, _ForeignKeyArtifactsIter]
]
_ForeignKeySchemaIter = typing.Iterable[typing.Tuple[str, types.Schema]]


def _calculate_foreign_key_property_artifacts(
    schemas: types.Schema,
    parent_name: str,
    parent_schema: types.Schema,
    property_name: str,
    property_schema: types.Schema,
) -> _ForeignKeyArtifacts:
    """
    Calculate the schema for the foreign key property.

    Assume the full relationship schema is valid.
    Assume that the relationship is not many-to-many

    Args:
        schemas: All defined schemas used to resolve any $ref.
        parent_name: The name of the schema that contains the relationship property.
        parent_schema: The schema that contains the relationship property.
        property_name: The name of the property.
        property_schema: The schema of the property.

    Returns:
        The schema of the foreign key property.

    """
    # Retrieve the schema of the property that is targeted by the foreign key
    relationship_type = oa_helpers.relationship.calculate_type(
        schema=property_schema, schemas=schemas
    )
    assert relationship_type != oa_helpers.relationship.Type.MANY_TO_MANY

    column_name = oa_helpers.foreign_key.calculate_column_name(
        type_=relationship_type, property_schema=property_schema, schemas=schemas,
    )
    target_schema = oa_helpers.foreign_key.get_target_schema(
        type_=relationship_type,
        parent_schema=parent_schema,
        property_schema=property_schema,
        schemas=schemas,
    )
    target_schema_properties = helpers.iterate.property_items(
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
    nullable = oa_helpers.peek.nullable(
        schema=foreign_key_target_schema, schemas=schemas
    )
    default = oa_helpers.peek.default(schema=foreign_key_target_schema, schemas=schemas)
    nullable = oa_helpers.calculate_nullable(
        nullable=nullable,
        generated=False,
        defaulted=default is not None,
        required=required,
    )

    # Retrieve information about the foreign key schema
    foreign_key = oa_helpers.foreign_key.calculate_foreign_key(
        column_name=column_name, target_schema=target_schema, schemas=schemas,
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

    return _ForeignKeyArtifacts(
        modify_name, foreign_key_property_name, foreign_key_property_schema
    )
