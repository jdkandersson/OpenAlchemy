"""Helpers for association tables."""

import typing

from ... import types
from ...helpers import foreign_key as foreign_key_helper
from ...helpers import peek
from ...helpers import relationship
from ..helpers import iterate


def _requires_association(schemas: types.Schemas, schema: types.Schema) -> bool:
    """
    Calculate whether a property requires an association table.

    Args:
        schema: The schema of the property to check.

    Returns:
        Whether the property requires an association table.

    """
    return relationship.is_relationship_type(
        type_=types.RelationshipType.MANY_TO_MANY, schema=schema, schemas=schemas
    )


class TParentPropertySchema(typing.NamedTuple):
    """Holds information about an association table."""

    parent: types.TNameSchema
    property: types.TNameSchema


def get_association_property_iterator(
    *, schemas: types.Schemas
) -> typing.Iterable[TParentPropertySchema]:
    """
    Get an iterator for properties that require association tables from the schemas.

    Assume that the schemas are individually valid.

    To ensure no duplication, property iteration stays within the model context.

    Args:
        schemas: All defined schemas.

    Returns:
        An iterator with properties that require an association table along with the
        schemas and the parent schema.

    """
    constructables = iterate.constructable(schemas=schemas)
    for name, schema in constructables:
        properties = iterate.properties_items(
            schema=schema, schemas=schemas, stay_within_model=True
        )
        association_property_schemas = filter(
            lambda args: _requires_association(schemas, args[1]), properties
        )
        yield from (
            TParentPropertySchema(
                parent=types.TNameSchema(name=name, schema=schema),
                property=types.TNameSchema(name=property_name, schema=property_schema),
            )
            for property_name, property_schema in association_property_schemas
        )


def get_secondary(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get the secondary value from a many-to-many relationship property.

    Assume that the property is a valid many-to-many relationship.

    Args:
        schema: The schema of the many-to-many property.
        schemas: All defined schemas.

    Returns:
        The value of x-secondary.

    """
    items = peek.items(schema=schema, schemas=schemas)
    assert items is not None
    secondary = peek.prefer_local(
        get_value=peek.secondary, schema=items, schemas=schemas
    )
    assert secondary is not None and isinstance(secondary, str)
    return secondary


def get_secondary_parent_property_schema_mapping(
    *, schemas: types.Schemas
) -> typing.Dict[str, TParentPropertySchema]:
    """
    Get a mapping keyed with the x-secondary value and the parent and property schema.

    Assume that the schemas are individually valid.

    To ensure no duplication, property iteration stays within the model context.

    Args:
        schemas: All defined schemas.

    Returns:
        A dictionary with the x-secondary value is the key and the parent and property
        schema of an association as the value.

    """
    association_properties = get_association_property_iterator(schemas=schemas)
    association_name_parent_property_schemas = map(
        lambda association: (
            get_secondary(schema=association.property.schema, schemas=schemas),
            association,
        ),
        association_properties,
    )
    return dict(association_name_parent_property_schemas)


class TCalculatePropertySchemaReturn(typing.NamedTuple):
    """The return type for the calculate_property_schema function."""

    name: str
    schema: types.ColumnSchema


def calculate_property_schema(
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
    properties = iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_tablename=True
    )
    primary_key_properties = filter(
        lambda args: peek.primary_key(schema=args[1], schemas=schemas) is True,
        properties,
    )
    primary_key_property = next(primary_key_properties, None)
    assert primary_key_property is not None
    assert next(primary_key_properties, None) is None

    # Get artifacts
    tablename = peek.prefer_local(
        get_value=peek.tablename, schema=schema, schemas=schemas
    )
    primary_key_property_name, primary_key_property_schema = primary_key_property
    type_ = peek.type_(schema=primary_key_property_schema, schemas=schemas)
    format_ = peek.format_(schema=primary_key_property_schema, schemas=schemas)
    max_length = peek.max_length(schema=primary_key_property_schema, schemas=schemas)
    foreign_key = foreign_key_helper.calculate_foreign_key(
        column_name=primary_key_property_name, target_schema=schema, schemas=schemas
    )

    # Calculate name and schema
    property_name = f"{tablename}_{primary_key_property_name}"
    property_schema: types.ColumnSchema = {
        types.OpenApiProperties.TYPE.value: type_,
        types.ExtensionProperties.PRIMARY_KEY.value: True,
        types.ExtensionProperties.FOREIGN_KEY.value: foreign_key,
    }
    if format_ is not None:
        property_schema[types.OpenApiProperties.FORMAT.value] = format_
    if max_length is not None:
        property_schema[types.OpenApiProperties.MAX_LENGTH.value] = max_length

    return TCalculatePropertySchemaReturn(name=property_name, schema=property_schema)


def calculate_schema(
    *,
    property_schema: types.Schema,
    parent_schema: types.Schema,
    schemas: types.Schemas,
) -> types.TNameSchema:
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

    The following is the form of the schema:
    <association schema name>:
        type: object
        x-tablename: <x-secondary>
        properties:
            <parent tablename>_<parent property name>:
                type: <parent property type>
                x-primary-key: true
                # if the parent property defines a format
                format: <parent property format>
                # if the parent property defines maxLength
                maxLength: <parent property maxLength>
                x-foreign-key: <parent tablename>.<parent property name>
            <child tablename>_<child property name>:
                type: <child property type>
                x-primary-key: true
                # if the child property defines a format
                format: <child property format>
                # if the child property defines maxLength
                maxLength: <child property maxLength>
                x-foreign-key: <child tablename>.<child property name>
        required:
            - <parent tablename>_<parent property name>
            - <child tablename>_<child property name>

    Args:
        parent_schema: The schema the property is embedded in.
        property_schema: The schema of the many-to-many property.
        schemas: All defined schemas.

    Returns:
        The schema of the association table.

    """
    secondary = get_secondary(schema=property_schema, schemas=schemas)
    parent_property = calculate_property_schema(schema=parent_schema, schemas=schemas)
    _, ref_schema = relationship.get_ref_schema_many_to_x(
        property_schema=property_schema, schemas=schemas
    )
    ref_property = calculate_property_schema(schema=ref_schema, schemas=schemas)

    schema = {
        types.OpenApiProperties.TYPE: "object",
        types.ExtensionProperties.TABLENAME: secondary,
        types.OpenApiProperties.PROPERTIES: {
            parent_property.name: parent_property.schema,
            ref_property.name: ref_property.schema,
        },
        types.OpenApiProperties.REQUIRED: [parent_property.name, ref_property.name],
    }

    name = secondary.title().replace("_", "")
    while name in schemas:
        name = f"Autogen{name}"

    return types.TNameSchema(name=name, schema=schema)
