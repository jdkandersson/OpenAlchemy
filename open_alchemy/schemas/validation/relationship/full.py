"""Validate the full schema (property, source and referenced)."""

# pylint: disable=unused-argument,unused-variable

import itertools

from .... import exceptions
from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import simple
from .. import types


def _check_foreign_key_target_schema(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas, foreign_key_column: str
) -> types.OptResult:
    """
    Check the schema that is targeted by a foreign key.

    Args:
        schema: The schema targeted by a foreign key.
        schemas: The schemas used to resolve any $ref.
        foreign_key_column: The name of the foreign key column.

    Returns:
        A result if something is wrong with the reason or None otherwise.

    """
    # Check tablename
    try:
        tablename = oa_helpers.peek.tablename(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return types.Result(False, "value of x-tablename must be a string")
    if tablename is None:
        return types.Result(False, "referenced schema must have a x-tablename value")

    # Check properties
    properties = helpers.iterate.properties(schema=schema, schemas=schemas)
    has_one_property = next(properties, None)
    if has_one_property is None:
        return types.Result(False, "referenced schema must have properties")
    properties = itertools.chain([has_one_property], properties)

    # Look for foreign key property schema
    filtered_properties = filter(lambda arg: arg[0] == foreign_key_column, properties)
    foreign_key_target_property = next(filtered_properties, None)
    if foreign_key_target_property is None:
        return types.Result(
            False, f"referenced schema must have the {foreign_key_column} property"
        )

    # Validate the schema
    (
        foreign_key_target_property_name,
        foreign_key_target_property_schema,
    ) = foreign_key_target_property
    schema_result = simple.check(schemas, foreign_key_target_property_schema)
    if not schema_result.valid:
        return types.Result(
            False,
            f"malformed referenced schema for {foreign_key_target_property_name} "
            f"property: {schema_result.reason}",
        )

    return None


def _check_x_to_many(
    *,
    schemas: oa_types.Schemas,
    source_schema: oa_types.Schema,
    property_name: str,
    property_schema: oa_types.Schema,
) -> types.Result:
    """Check x-to-many relationships."""
    foreign_key_target_name, foreign_key_target_schema = oa_helpers.ref.resolve(
        name=property_name, schema=property_schema, schemas=schemas
    )

    # Calculate the foreign key name
    foreign_key_column = oa_helpers.peek.foreign_key_column(
        schema=property_schema, schemas=schemas
    )
    if foreign_key_column is None:
        foreign_key_column = "id"

    # Check foreign key target schema
    foreign_key_target_schema_result = _check_foreign_key_target_schema(
        schema=foreign_key_target_schema,
        schemas=schemas,
        foreign_key_column=foreign_key_column,
    )
    if foreign_key_target_schema_result is not None:
        return foreign_key_target_schema_result

    return types.Result(True, None)


def check(
    schemas: oa_types.Schemas,
    source_schema: oa_types.Schema,
    property_name: str,
    property_schema: oa_types.Schema,
) -> types.Result:
    """
    Check the source, referenced and property schema.

    Assume the property schema validation is already complete.

    At a high level:
    1. either an id or the column configured by x-foreign-key-column must be on the
        schema the foreign key points at,
    2. the property the foreign key points at must
        a. have a valid type and not object nor array and
        b. must have valid values for format, nullable, maxLength and default if they
            are defined
    3. the schema the foreign key points at must define a tablename except for
        many-to-many relationships,
    4. if a property on the schema the foreign key points at with the same name as the
        foreign key is already defined then it must match the following information:
        a. type,
        b. format,
        c. maxLength,
        d. default and
        e. have the same foreign key constraint as defined by the relationship,
    5. for many-to-many relationships both the source and referenced schema must have
        have a single primary key column with a valid type that is not an object nor an
        array and
    6. for many-to-many relationships both the source and referenced schema must have a
        single valid primary key property.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        source_schema: The schema that has the property embedded in it.
        property_name: The name of the property.
        property_schema: The schema of the property.

    Returns:
        WHether the full relationship schema is valid and, if not, why it isn't.

    """
    type_ = oa_helpers.peek.type_(schema=property_schema, schemas=schemas)
    if type_ == "object":
        return _check_x_to_many(
            schemas=schemas,
            source_schema=source_schema,
            property_name=property_name,
            property_schema=property_schema,
        )

    return types.Result(True, None)
