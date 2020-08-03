"""Validate the full schema (property, source and referenced)."""

import itertools

from .... import exceptions
from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import simple
from .. import types


def _check_pre_defined_property_schema(
    *,
    property_name: str,
    property_schema: oa_types.Schema,
    schema: oa_types.Schema,
    schemas: oa_types.Schemas,
    foreign_key: str,
):
    """
    Check for a pre-defined property on a schema.

    Assume property_schema has already been checked for validity.

    Args:
        property_name: The expected foreign key property name to check for.
        property_schema: The schema for the foreign key.
        schema: The schema to check for the property on.
        schemas: Used to resolve any $ref.
        foreign_key: The foreign key value.

    Returns:
        A result if something is wrong with the reason or None otherwise.

    """
    # Get the pre-defined property schema if it exists
    properties = helpers.iterate.property_items(
        schema=schema, schemas=schemas, stay_within_tablename=True
    )
    filtered_properties = filter(lambda arg: arg[0] == property_name, properties)
    defined_property = next(filtered_properties, None)
    if defined_property is None:
        return None

    # Validate the schema
    _, defined_property_schema = defined_property
    schema_result = simple.check(schemas, defined_property_schema)
    if not schema_result.valid:
        return types.Result(
            False, f"{property_name} property :: {schema_result.reason}",
        )

    # Check that key information matches
    checks = (
        ("type", oa_helpers.peek.type_),
        ("format", oa_helpers.peek.format_),
        ("maxLength", oa_helpers.peek.max_length),
        ("default", oa_helpers.peek.default),
    )
    for key, func in checks:
        expected_value = func(schema=property_schema, schemas=schemas)
        if expected_value is None:
            expected_value_str = "not to be defined"
        else:
            expected_value_str = str(expected_value)
        actual_value = func(schema=defined_property_schema, schemas=schemas)
        if actual_value is None:
            actual_value_str = "not defined"
        else:
            actual_value_str = str(actual_value)
        if expected_value != actual_value:
            return types.Result(
                False,
                f"the {key} of {property_name} is wrong, expected "
                f"{expected_value_str}, actual is {actual_value_str}.",
            )

    # Check the foreign key
    actual_foreign_key = oa_helpers.peek.foreign_key(
        schema=defined_property_schema, schemas=schemas
    )
    if actual_foreign_key is None:
        return types.Result(False, f"{property_name} must define a foreign key",)
    if actual_foreign_key != foreign_key:
        return types.Result(
            False,
            f"the x-foreign-key of {property_name} is wrong, expected {foreign_key}, "
            f"the actual is {actual_foreign_key}",
        )

    return None


def _check_foreign_key_target_schema(
    *,
    foreign_key_target_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
    foreign_key_column_name: str,
    modify_schema: oa_types.Schema,
    foreign_key_property_name: str,
) -> types.OptResult:
    """
    Check the schema that is targeted by a foreign key.

    Args:
        foreign_key_target_schema: The schema targeted by a foreign key.
        schemas: The schemas used to resolve any $ref.
        foreign_key_column_name: The name of the foreign key column.
        modify_schema: The schema to add the foreign key property to.
        foreign_key_property_name: The name of the foreign key property to define.

    Returns:
        A result if something is wrong with the reason or None otherwise.

    """
    # Check tablename
    tablename = oa_helpers.peek.tablename(
        schema=foreign_key_target_schema, schemas=schemas
    )
    if tablename is None:
        return types.Result(
            False, "foreign key targeted schema must have a x-tablename value"
        )

    # Check properties
    properties = helpers.iterate.property_items(
        schema=foreign_key_target_schema, schemas=schemas, stay_within_tablename=True,
    )
    has_one_property = next(properties, None)
    if has_one_property is None:
        return types.Result(False, "foreign key targeted schema must have properties")
    properties = itertools.chain([has_one_property], properties)

    # Look for foreign key property schema
    filtered_properties = filter(
        lambda arg: arg[0] == foreign_key_column_name, properties
    )
    foreign_key_target_property = next(filtered_properties, None)
    if foreign_key_target_property is None:
        return types.Result(
            False,
            f"foreign key targeted schema must have the {foreign_key_column_name} "
            "property",
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
            f"{foreign_key_target_property_name} property :: {schema_result.reason}",
        )

    # Check for pre-defined foreign key property
    foreign_key = oa_helpers.foreign_key.calculate_foreign_key(
        tablename=tablename, foreign_key_column_name=foreign_key_column_name
    )
    pre_defined_result = _check_pre_defined_property_schema(
        property_name=foreign_key_property_name,
        property_schema=foreign_key_target_property_schema,
        schema=modify_schema,
        schemas=schemas,
        foreign_key=foreign_key,
    )
    if pre_defined_result is not None:
        return pre_defined_result

    return None


def _check_x_to_one(
    *,
    modify_schema: oa_types.Schema,
    property_name: str,
    property_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> types.Result:
    """
    Check x-to-one relationships.

    Args:
        modify_schema: The schema to which the foreign key property needs to be added.
        property_name: The name of the property that defines the x-to-one relationship.
        property_schema: The schema of the property that defines the x-to-one
            relationship.
        schemas: Used to result any $ref.

    Returns:
        Whether the relationship is valid and the reason if it is not.

    """
    type_ = oa_helpers.relationship.Type.MANY_TO_ONE

    _, foreign_key_target_schema = oa_helpers.ref.resolve(
        name=property_name, schema=property_schema, schemas=schemas
    )

    # Calculate the foreign key name
    foreign_key_column_name = oa_helpers.foreign_key.calculate_column_name(
        type_=type_, property_schema=property_schema, schemas=schemas,
    )

    # Check foreign key target schema
    foreign_key_property_name = oa_helpers.foreign_key.calculate_prop_name(
        type_=type_,
        column_name=foreign_key_column_name,
        property_name=property_name,
        target_schema=foreign_key_target_schema,
        schemas=schemas,
    )
    foreign_key_target_schema_result = _check_foreign_key_target_schema(
        foreign_key_target_schema=foreign_key_target_schema,
        schemas=schemas,
        foreign_key_column_name=foreign_key_column_name,
        modify_schema=modify_schema,
        foreign_key_property_name=foreign_key_property_name,
    )
    if foreign_key_target_schema_result is not None:
        return foreign_key_target_schema_result

    return types.Result(True, None)


def _check_one_to_many(
    *,
    foreign_key_target_schema: oa_types.Schema,
    property_name: str,
    property_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> types.Result:
    """
    Check one-to-many relationships.

    Assume foreign_key_target_schema has already been validated.

    Args:
        foreign_key_target_schema: The schema targeted by the foreign key.
        property_name: The name of the property that defines the one-to-many
            relationship.
        property_schema: The schema of the property that defines the one-to-many
            relationship.
        schemas: Used to result any $ref.

    Returns:
        Whether the relationship is valid and the reason if it is not.

    """
    type_ = oa_helpers.relationship.Type.ONE_TO_MANY

    # Retrieve the items schema
    items_schema = oa_helpers.peek.items(schema=property_schema, schemas=schemas)
    assert items_schema is not None

    # Calculate the foreign key name
    foreign_key_column_name = oa_helpers.foreign_key.calculate_column_name(
        type_=type_, property_schema=property_schema, schemas=schemas,
    )

    # Retrieve the schema the foreign key needs to go onto
    modify_schema_ref = oa_helpers.peek.ref(schema=items_schema, schemas=schemas)
    _, modify_schema = oa_helpers.ref.resolve(
        schema={"$ref": modify_schema_ref}, schemas=schemas, name=""
    )

    # Calculate the foreign key property name
    tablename = oa_helpers.peek.tablename(
        schema=foreign_key_target_schema, schemas=schemas
    )
    if tablename is None:
        return types.Result(
            False, "foreign key targeted schema must have a x-tablename value"
        )
    foreign_key_property_name = oa_helpers.foreign_key.calculate_prop_name(
        type_=type_,
        column_name=foreign_key_column_name,
        property_name=property_name,
        target_schema=foreign_key_target_schema,
        schemas=schemas,
    )
    foreign_key_target_schema_result = _check_foreign_key_target_schema(
        foreign_key_target_schema=foreign_key_target_schema,
        schemas=schemas,
        foreign_key_column_name=foreign_key_column_name,
        modify_schema=modify_schema,
        foreign_key_property_name=foreign_key_property_name,
    )
    if foreign_key_target_schema_result is not None:
        return foreign_key_target_schema_result

    return types.Result(True, None)


def _check_many_to_many_schema(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """
    Check one of the many to many schemas.

    Args:
        schema: The schema to check.
        schemas: Used to resolve any $ref.

    Returns:
        A result of the schema is not valid with a reason or None.

    """
    tablename = oa_helpers.peek.tablename(schema=schema, schemas=schemas)
    if tablename is None:
        return types.Result(False, "schema must define x-tablename")

    # Check for primary key
    properties = helpers.iterate.property_items(
        schema=schema, schemas=schemas, stay_within_tablename=True
    )
    primary_key_properties = filter(
        lambda args: oa_helpers.peek.primary_key(schema=args[1], schemas=schemas)
        is True,
        properties,
    )
    primary_key_property = next(primary_key_properties, None)
    if primary_key_property is None:
        return types.Result(False, "schema must have a primary key")

    # Check for multiple primary keys
    next_primary_key_property = next(primary_key_properties, None)
    if next_primary_key_property is not None:
        return types.Result(
            False,
            "many-to-many relationships currently only support single primary key "
            "schemas",
        )

    # Check property schema
    primary_key_property_name, primary_key_property_schema = primary_key_property
    schema_result = simple.check(schemas, primary_key_property_schema)
    if schema_result.valid is False:
        return types.Result(
            False, f"{primary_key_property_name} property :: {schema_result.reason}"
        )

    return None


def _check_many_to_many(
    *,
    parent_schema: oa_types.Schema,
    property_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> types.Result:
    """
    Check many-to-many relationships.

    Args:
        parent_schema: The schema that has the property that defines the relationship.
        property_schema: The schema of the items for the property that defines the
            relationship.
        schemas: Used to resolve any $ref.

    Returns:
        Whether the relationship is valid and the reason if it is not.

    """
    # Checking source schema
    source_result = _check_many_to_many_schema(schema=parent_schema, schemas=schemas)
    if source_result is not None:
        return types.Result(
            source_result.valid, f"source schema :: {source_result.reason}"
        )

    # Checking referenced schema
    items_schema = oa_helpers.peek.items(schema=property_schema, schemas=schemas)
    assert items_schema is not None
    ref = oa_helpers.peek.ref(schema=items_schema, schemas=schemas)
    _, ref_schema = oa_helpers.ref.resolve(
        schema={"$ref": ref}, schemas=schemas, name=""
    )
    ref_result = _check_many_to_many_schema(schema=ref_schema, schemas=schemas)
    if ref_result is not None:
        return types.Result(
            ref_result.valid, f"referenced schema :: {ref_result.reason}"
        )

    return types.Result(True, None)


def check(
    schemas: oa_types.Schemas,
    parent_schema: oa_types.Schema,
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
        parent_schema: The schema that has the property embedded in it.
        property_name: The name of the property.
        property_schema: The schema of the property.

    Returns:
        WHether the full relationship schema is valid and, if not, why it isn't.

    """
    try:
        type_ = oa_helpers.relationship.calculate_type(
            schema=property_schema, schemas=schemas
        )
        if type_ in {
            oa_helpers.relationship.Type.MANY_TO_ONE,
            oa_helpers.relationship.Type.ONE_TO_ONE,
        }:
            return _check_x_to_one(
                schemas=schemas,
                modify_schema=parent_schema,
                property_name=property_name,
                property_schema=property_schema,
            )
        if type_ == oa_helpers.relationship.Type.ONE_TO_MANY:
            return _check_one_to_many(
                schemas=schemas,
                foreign_key_target_schema=parent_schema,
                property_name=property_name,
                property_schema=property_schema,
            )
        return _check_many_to_many(
            parent_schema=parent_schema,
            property_schema=property_schema,
            schemas=schemas,
        )

    except exceptions.MalformedSchemaError as exc:
        return types.Result(False, f"malformed schema :: {exc}")
