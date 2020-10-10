"""Pre-process schemas by adding any association tables as a schema to schemas."""

import typing

from .. import types
from .. import helpers as oa_helpers
from . import helpers


class TCalculatePropertySchemaReturn(typing.NamedTuple):
    """The return type for the _calculate_property_schema function."""

    name: str
    schema: types.ColumnSchema


def _calculate_property_schema(
    *, schema: types.Schema, schemas: types.Schemas
) -> TCalculatePropertySchemaReturn:
    """
    Calculate the property name and schema for a column for a many-to-many relationship.

    Assume that all schemas are valid.
    Assume that the schema has a single primary key.

    The following algorithm is used to calculate key artifacts:
    - the type is the type of the primary key property of the schema
    - if defined on the primary key property, the format is the format of the primary
        key property
    - if defined on the primary key property, the maxLength is the maxLength of the
        primary key property
    - the primary key is set to True
    - the foreign key is <schema tablename>.<primary key property name>
    - the property name is <schema tablename>_<primary key property name>

    Args:
        schemas: All defined schemas.
        schema: The model schema to use to calculate the property schema.

    Returns:
        The property name and schema for one of the columns of the association table
        that handles one of the sides of the many to many relationship.

    """
    # Retrieve primary key column
    properties = helpers.iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_tablename=True
    )
    primary_key_properties = filter(
        lambda args: oa_helpers.peek.primary_key(schema=args[1], schemas=schemas)
        is True,
        properties,
    )
    primary_key_property = next(primary_key_properties, None)
    assert primary_key_property is not None
    assert next(primary_key_properties, None) is None

    # Get artifacts
    tablename = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.tablename, schema=schema, schemas=schemas
    )
    primary_key_property_name, primary_key_property_schema = primary_key_property
    type_ = oa_helpers.peek.type_(schema=primary_key_property_schema, schemas=schemas)
    format_ = oa_helpers.peek.format_(
        schema=primary_key_property_schema, schemas=schemas
    )
    max_length = oa_helpers.peek.max_length(
        schema=primary_key_property_schema, schemas=schemas
    )
    foreign_key = oa_helpers.foreign_key.calculate_foreign_key(
        column_name=primary_key_property_name, target_schema=schema, schemas=schemas
    )

    # Calculate name and schema
    property_name = f"{tablename}_{primary_key_property_name}"
    property_schema: types.ColumnSchema = {
        "type": type_,
        "x-primary-key": True,
        "x-foreign-key": foreign_key,
    }
    if format_ is not None:
        property_schema["format"] = format_
    if max_length is not None:
        property_schema["maxLength"] = max_length

    return TCalculatePropertySchemaReturn(name=property_name, schema=property_schema)
