"""Pre-process schemas by adding any association tables as a schema to schemas."""

import typing

from .. import helpers as oa_helpers
from .. import types
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


class TCalculateSchemaReturn(typing.NamedTuple):
    """The return type for the _calculate_schema function."""

    name: str
    schema: types.Schema


def _calculate_schema(
    *,
    parent_schema: types.Schema,
    property_schema: types.Schema,
    schemas: types.Schemas,
) -> TCalculateSchemaReturn:
    """
    Calculate the schema for the association table.

    Assume that all schemas are valid.
    Assume that the property schema is a many-to-many relationship.

    The following algorithm is used to calculate the schema:
    1. retrieve the secondary value,
    2. calculate the property schema for the parent schema,
    3. retrieve the referenced schema and calculate the property schema,
    4. assemble the final schema with
        a. the object type,
        b. tablename of the secondary value,
        c. properties based on the parent and referenced schema and
        d. required with the property names and
    5. calculate the schema name based on the secondary value and avoiding any existing
        schema names.

    Args:
        parent_schema: The schema the property is embedded in.
        property_schema: The schema of the many-to-many property.
        schemas: All defined schemas.

    Returns:
        The schema of the association table.

    """
    items = oa_helpers.peek.items(schema=property_schema, schemas=schemas)
    assert items is not None
    secondary = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.secondary, schema=items, schemas=schemas
    )
    assert secondary is not None and isinstance(secondary, str)

    parent_property = _calculate_property_schema(schema=parent_schema, schemas=schemas)

    _, ref_schema = oa_helpers.relationship.get_ref_schema_many_to_x(
        property_schema=property_schema, schemas=schemas
    )
    ref_property = _calculate_property_schema(schema=ref_schema, schemas=schemas)

    schema = {
        "type": "object",
        "x-tablename": secondary,
        "properties": {
            parent_property.name: parent_property.schema,
            ref_property.name: ref_property.schema,
        },
        "required": [parent_property.name, ref_property.name],
    }

    name = secondary.title().replace("_", "")
    while name in schemas:
        name = f"Autogen{name}"

    return TCalculateSchemaReturn(name=name, schema=schema)
