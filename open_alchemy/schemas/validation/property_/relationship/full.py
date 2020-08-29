"""Validate the full schema (property, source and referenced)."""

from ..... import exceptions
from ..... import helpers as oa_helpers
from ..... import types as oa_types
from .... import helpers
from ... import helpers as validation_helpers
from ... import model
from ... import types
from .. import simple


def _check_value_matches(
    *,
    func: oa_helpers.peek.PeekValue,
    reference_schema: oa_types.Schema,
    check_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> types.OptResult:
    """
    Check that the value matches in two schemas.

    Args:
        func: Used to retrieve the value.
        reference_schema: The schema to check against.
        check_schema: The schema to check
        schemas: All defined schemas, used to resolve any $ref.

    Returns:
        An invalid result with reason if the values don't match otherwise None.

    """
    expected_value = func(schema=reference_schema, schemas=schemas)
    if expected_value is None:
        expected_value_str = "not to be defined"
    else:
        expected_value_str = str(expected_value)

    actual_value = func(schema=check_schema, schemas=schemas)
    if actual_value is None:
        actual_value_str = "not defined"
    else:
        actual_value_str = str(actual_value)

    if expected_value != actual_value:
        return types.Result(
            False,
            f"expected {expected_value_str}, actual is {actual_value_str}.",
        )

    return None


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
    properties = helpers.iterate.properties_items(
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
            False,
            f"{property_name} property :: {schema_result.reason}",
        )

    # Check that key information matches
    checks = (
        ("type", oa_helpers.peek.type_),
        ("format", oa_helpers.peek.format_),
        ("maxLength", oa_helpers.peek.max_length),
        ("default", oa_helpers.peek.default),
    )
    for key, func in checks:
        match_result = _check_value_matches(
            func=func,
            reference_schema=property_schema,
            check_schema=defined_property_schema,
            schemas=schemas,
        )
        if match_result is None:
            continue

        return types.Result(
            match_result.valid, f"{property_name} :: {key} :: {match_result.reason}"
        )

    # Check the foreign key
    actual_foreign_key = oa_helpers.peek.foreign_key(
        schema=defined_property_schema, schemas=schemas
    )
    if actual_foreign_key is None:
        return types.Result(
            False,
            f"{property_name} must define a foreign key",
        )
    if actual_foreign_key != foreign_key:
        return types.Result(
            False,
            f"the x-foreign-key of {property_name} is wrong, expected {foreign_key}, "
            f"the actual is {actual_foreign_key}",
        )

    return None


def _check_target_schema(
    *,
    target_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
    column_name: str,
    modify_schema: oa_types.Schema,
    foreign_key_property_name: str,
) -> types.Result:
    """
    Check the schema that is targeted by a foreign key.

    Assume target_schema is valid.

    Args:
        target_schema: The schema targeted by a foreign key.
        schemas: The schemas used to resolve any $ref.
        column_name: The name of the foreign key column.
        modify_schema: The schema to add the foreign key property to.
        foreign_key_property_name: The name of the foreign key property to define.

    Returns:
        A result if something is wrong with the reason or None otherwise.

    """
    # Look for foreign key property schema
    properties = helpers.iterate.properties_items(
        schema=target_schema,
        schemas=schemas,
        stay_within_tablename=True,
    )
    filtered_properties = filter(lambda arg: arg[0] == column_name, properties)
    foreign_key_target_property = next(filtered_properties, None)
    if foreign_key_target_property is None:
        return types.Result(
            False,
            f"foreign key targeted schema must have the {column_name} property",
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
        column_name=column_name,
        target_schema=target_schema,
        schemas=schemas,
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
    model_result = model.check(schema=schema, schemas=schemas)
    if not model_result.valid:
        return model_result

    # Check for primary key
    properties = helpers.iterate.properties_items(
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
    assert ref is not None
    _, ref_schema = oa_helpers.ref.get_ref(ref=ref, schemas=schemas)
    ref_result = _check_many_to_many_schema(schema=ref_schema, schemas=schemas)
    if ref_result is not None:
        return types.Result(
            ref_result.valid, f"referenced schema :: {ref_result.reason}"
        )

    return types.Result(True, None)


def _check_backref_property_properties_basics(
    property_name: str,
    backref_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> types.OptResult:
    """
    Check the backref schema.

    Args:
        parent_schema: The schema that has the property embedded in it.
        property_name: The name of the property.
        backref_schema: The schema of the back reference.
        schemas: All defined schemas used to resolve any $ref.
    """
    # Check for object type
    type_ = oa_helpers.peek.type_(schema=backref_schema, schemas=schemas)
    if type_ != "object":
        return types.Result(False, "the back reference schema must be an object")

    # Check properties values
    properties_values_result = validation_helpers.properties.check_properties_values(
        schema=backref_schema, schemas=schemas
    )
    if properties_values_result is not None:
        return properties_values_result

    # Check whether any property names match the property name
    properties_items = helpers.iterate.properties_items(
        schema=backref_schema, schemas=schemas
    )
    property_name_matches = next(
        filter(lambda args: args[0] == property_name, properties_items), None
    )
    if property_name_matches is not None:
        return types.Result(
            False,
            "properties cannot contain the property name of the relartionship to avoid "
            "circular references",
        )

    return None


def _check_backref_property_properties(
    parent_schema: oa_types.Schema,
    property_name: str,
    backref_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> types.OptResult:
    """
    Check the backref schema.

    Args:
        parent_schema: The schema that has the property embedded in it.
        property_name: The name of the property.
        backref_schema: The schema of the back reference.
        schemas: All defined schemas used to resolve any $ref.
    """
    basics_result = _check_backref_property_properties_basics(
        property_name=property_name, backref_schema=backref_schema, schemas=schemas
    )
    if basics_result is not None:
        return basics_result

    # Check for backreference properties not in the parent schema properties
    parent_properties_items = helpers.iterate.properties_items(
        schema=parent_schema, schemas=schemas
    )
    parent_properties = dict(parent_properties_items)
    properties_items = helpers.iterate.properties_items(
        schema=backref_schema, schemas=schemas
    )
    property_name_not_in_parent = next(
        filter(lambda args: args[0] not in parent_properties, properties_items), None
    )
    if property_name_not_in_parent is not None:
        name, _ = property_name_not_in_parent
        return types.Result(False, f"could not find {name} in the model schema")

    # Check properties are dictionaries
    properties_items_result = validation_helpers.properties.check_properties_items(
        schema=backref_schema, schemas=schemas
    )
    if properties_items_result is not None:
        return properties_items_result

    # Check schema matches
    checks = (
        ("type", oa_helpers.peek.type_),
        ("format", oa_helpers.peek.format_),
        ("maxLength", oa_helpers.peek.max_length),
        ("default", oa_helpers.peek.default),
    )
    for key, func in checks:
        properties_items = helpers.iterate.properties_items(
            schema=backref_schema, schemas=schemas
        )
        # pylint: disable=cell-var-from-loop
        # Calculate result for each property
        properties_items_value_results = map(
            lambda args: (
                args[0],
                _check_value_matches(
                    func=func,
                    reference_schema=parent_properties[args[0]],
                    check_schema=args[1],
                    schemas=schemas,
                ),
            ),
            properties_items,
        )
        # Look for the first failed result
        properties_items_value_result = next(
            filter(lambda args: args[1] is not None, properties_items_value_results),
            None,
        )
        if properties_items_value_result is not None:
            property_name, result = properties_items_value_result
            assert result is not None
            return types.Result(
                result.valid, f"{property_name} :: {key} :: {result.reason}"
            )

    return None


_BACKREF_EXPECTED_TYPE = {
    oa_helpers.relationship.Type.MANY_TO_ONE: "array",
    oa_helpers.relationship.Type.ONE_TO_ONE: "object",
    oa_helpers.relationship.Type.ONE_TO_MANY: "object",
    oa_helpers.relationship.Type.MANY_TO_MANY: "array",
}


def _check_backref_property(
    parent_schema: oa_types.Schema,
    property_name: str,
    relationship_type: oa_helpers.relationship.Type,
    backref_property_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> types.OptResult:
    """Check the back reference property."""
    # Check the type of the property
    read_only = oa_helpers.peek.read_only(
        schema=backref_property_schema, schemas=schemas
    )
    if not read_only:
        return types.Result(False, "the property must be readOnly")

    # Check the type of the backref property
    property_type = oa_helpers.peek.type_(
        schema=backref_property_schema, schemas=schemas
    )
    expected_property_type = _BACKREF_EXPECTED_TYPE[relationship_type]
    if expected_property_type != property_type:
        return types.Result(
            False,
            f"unexpected type, expected {expected_property_type} actual "
            f"{property_type}",
        )

    # Check the properties
    if relationship_type in {
        oa_helpers.relationship.Type.MANY_TO_ONE,
        oa_helpers.relationship.Type.MANY_TO_MANY,
    }:
        items_schema = oa_helpers.peek.items(
            schema=backref_property_schema, schemas=schemas
        )
        if items_schema is None:
            return types.Result(False, "items must be defined")
        properties_result = _check_backref_property_properties(
            parent_schema=parent_schema,
            property_name=property_name,
            backref_schema=items_schema,
            schemas=schemas,
        )
        if properties_result is not None:
            return types.Result(
                False, f"items :: properties :: {properties_result.reason}"
            )
    else:
        properties_result = _check_backref_property_properties(
            parent_schema=parent_schema,
            property_name=property_name,
            backref_schema=backref_property_schema,
            schemas=schemas,
        )
        if properties_result is not None:
            return types.Result(False, f"properties :: {properties_result.reason}")
    return None


def _check_backref(
    parent_schema: oa_types.Schema,
    property_name: str,
    relationship_type: oa_helpers.relationship.Type,
    property_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> types.OptResult:
    """
    Check the back reference, if defined.

    Assume the property schema and parent schema is valid.

    Algorithm:
        1. check for back reference, if not there stop,
        2. check for whether back reference value is in the properties, if not stop,
        3. check the type of the property based on the relationship type,
        4. if the back reference is an array, retrieve the items schema
        5. check whether the properties are valid,
        6. check that the property being processed is not in the properties,
        6. check that all defined properties are also on the parent schema and
        7. check that the type and format match.

    Args:
        parent_schema: The schema that has the property embedded in it.
        property_name: The name of the property.
        relationship_type: The type of the relationship the property defines.
        property_schema: The schema of the property.
        schemas: All defined schemas used to resolve any $ref.

    Returns:
        If the back reference is invalid, returns result with reason, otherwise None.

    """
    backref = helpers.backref.get(schema=property_schema, schemas=schemas)
    if backref is None:
        return None

    # Get the object schema
    object_schema: oa_types.Schema
    if relationship_type in {
        oa_helpers.relationship.Type.ONE_TO_MANY,
        oa_helpers.relationship.Type.MANY_TO_MANY,
    }:
        items_schema = oa_helpers.peek.items(schema=property_schema, schemas=schemas)
        assert items_schema is not None
        object_schema = items_schema
    else:
        object_schema = property_schema

    # Look for backref property
    properties = helpers.iterate.properties_items(schema=object_schema, schemas=schemas)
    property_ = next(filter(lambda args: args[0] == backref, properties), None)
    if property_ is None:
        return None
    _, backref_property_schema = property_

    try:
        return _check_backref_property(
            parent_schema=parent_schema,
            property_name=property_name,
            relationship_type=relationship_type,
            backref_property_schema=backref_property_schema,
            schemas=schemas,
        )

    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")


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
            oa_helpers.relationship.Type.ONE_TO_MANY,
        }:
            # Retrieve information required to check x-to-one and one-to-many
            # relationships
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
            target_schema_model_result = model.check(
                schema=target_schema, schemas=schemas
            )
            if not target_schema_model_result.valid:
                return types.Result(
                    False,
                    f"foreign key target schema :: {target_schema_model_result.reason}",
                )
            modify_schema = oa_helpers.foreign_key.get_modify_schema(
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
            result = _check_target_schema(
                target_schema=target_schema,
                schemas=schemas,
                column_name=column_name,
                modify_schema=modify_schema,
                foreign_key_property_name=foreign_key_property_name,
            )
            if not result.valid:
                return result
        else:
            result = _check_many_to_many(
                parent_schema=parent_schema,
                property_schema=property_schema,
                schemas=schemas,
            )
            if not result.valid:
                return result

        backref_result = _check_backref(
            parent_schema=parent_schema,
            property_name=property_name,
            relationship_type=type_,
            property_schema=property_schema,
            schemas=schemas,
        )
        if backref_result is not None:
            return types.Result(
                backref_result.valid, f"backref property :: {backref_result.reason}"
            )

        return types.Result(True, None)

    except exceptions.MalformedSchemaError as exc:
        return types.Result(False, f"malformed schema :: {exc}")
