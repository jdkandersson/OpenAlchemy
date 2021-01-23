"""Validate association tables."""

import typing

from ... import types as oa_types
from ...helpers import peek
from ..helpers import association as association_helper
from ..helpers import iterate
from . import types
from .helpers import value


class _TNameSchemaTablename(typing.NamedTuple):
    """Holds the name, schema and tablename of a schema."""

    name: str
    schema: oa_types.Schema
    tablename: str


def _get_defined_association_iterator(
    schemas: oa_types.Schemas, tablename_mapping: typing.Dict[str, typing.Any]
) -> typing.Iterable[_TNameSchemaTablename]:
    """
    Get an iterator with schemas that have a tablename as defined by a mapping.

    Assume that individual schemas are valid.

    Algorithm:
    1. iterate over constructable schemas
    2. include any with an x-tablename value that appears in the tablename mapping

    Args:
        schemas: All defined schemas.
        tablename_mapping: A mapping of tablename to some value. Keys are used to
            indicate to include a schema.

    Returns:
        An iterator with all schemas that have their x-tablename appear in the
        tablename mapping.

    """
    constructables = iterate.constructable(schemas=schemas)
    constructables_tablename = map(
        lambda args: _TNameSchemaTablename(
            name=args[0],
            schema=args[1],
            tablename=peek.prefer_local(
                get_value=peek.tablename, schema=args[1], schemas=schemas
            ),
        ),
        constructables,
    )
    return filter(
        lambda args: args.tablename in tablename_mapping,
        constructables_tablename,
    )


def _primary_key_property_items_iterator(
    schema: oa_types.Schema, schemas: oa_types.Schemas
) -> typing.Iterator[typing.Tuple[str, oa_types.Schema]]:
    """
    Get an iterable with only primary key properties.

    Args:
        schema: The schema to get primary key properties from.
        schemas: All defined schemas.

    Returns:
        An iterator with all primary key properties.

    """
    properties = iterate.properties_items(schema=schema, schemas=schemas)
    return filter(
        lambda args: peek.prefer_local(
            get_value=peek.primary_key,
            schema=args[1],
            schemas=schemas,
        ),
        properties,
    )


def _check_2_or_fewer_primary_key(
    name: str,
    schema: oa_types.Schema,
    association: association_helper.TParentPropertySchema,
    schemas: oa_types.Schemas,
) -> types.Result:
    """
    Check that at most 2 primary key columns have been defined.

    Args:
        name: The name of the schema.
        schema: The schema to validate.
        association: Information about the association property.
        schemas: All defined schemas.

    Returns:
        Whether the schema is valid with a reason if it is not.

    """
    # Get first primary key property without foreign key
    primary_key_properties = _primary_key_property_items_iterator(schema, schemas)
    primary_key_count = sum(1 for _ in primary_key_properties)

    if primary_key_count > 2:
        return types.Result(
            valid=False,
            reason=(
                f'schema "{name}" defines more than 2 primary keys which is too many '
                "because it implements an association table for the many-to-many "
                f'relationship property "{association.property.name}" on the schema '
                f'"{association.parent.name}"'
            ),
        )

    return types.Result(valid=True, reason=None)


def _check_primary_key_no_foreign_key(
    name: str,
    schema: oa_types.Schema,
    association: association_helper.TParentPropertySchema,
    schemas: oa_types.Schemas,
) -> types.Result:
    """
    Check that all primary keys define foreign keys.

    Args:
        name: The name of the schema.
        schema: The schema to validate.
        association: Information about the association property.
        schemas: All defined schemas.

    Returns:
        Whether the schema is valid with a reason if it is not.

    """
    # Get first primary key property without foreign key
    primary_key_properties = _primary_key_property_items_iterator(schema, schemas)
    not_foreign_key_primary_key_properties = filter(
        lambda args: peek.foreign_key(schema=args[1], schemas=schemas) is None,
        primary_key_properties,
    )

    # Check for whether a primary key does not define a foreign key
    property_ = next(not_foreign_key_primary_key_properties, None)
    if property_ is not None:
        property_name, _ = property_
        return types.Result(
            valid=False,
            reason=(
                f'property "{property_name}" on schema "{name}" is a primary key and '
                "therefore must define a foreign key because it implements an "
                "association table for the many-to-many relationship property "
                f'"{association.property.name}" on the schema '
                f'"{association.parent.name}"'
            ),
        )

    return types.Result(valid=True, reason=None)


def _assert_str(item: typing.Any) -> str:
    """Check that item is a string."""
    assert isinstance(item, str)
    return item


def _check_duplicate_foreign_key(
    name: str,
    schema: oa_types.Schema,
    association: association_helper.TParentPropertySchema,
    schemas: oa_types.Schemas,
) -> types.Result:
    """
    Check that all primary key foreign keys are unique.

    Assume that all primary keys define a foreign key.

    Args:
        name: The name of the schema.
        schema: The schema to validate.
        association: Information about the association property.
        schemas: All defined schemas.

    Returns:
        Whether the schema is valid with a reason if it is not.

    """
    # Get first primary key property without foreign key
    primary_key_properties = _primary_key_property_items_iterator(schema, schemas)
    foreign_keys = map(
        lambda args: (
            args[0],
            peek.prefer_local(
                get_value=peek.foreign_key, schema=args[1], schemas=schemas
            ),
        ),
        primary_key_properties,
    )
    # Check that items are a string
    foreign_keys = map(lambda args: (args[0], _assert_str(args[1])), foreign_keys)

    # Check for duplicate foreign keys
    seen_foreign_keys: typing.Dict[str, str] = {}
    for property_name, foreign_key in foreign_keys:
        if foreign_key not in seen_foreign_keys:
            seen_foreign_keys[foreign_key] = property_name
            continue

        seen_on_property_name = seen_foreign_keys[foreign_key]
        return types.Result(
            valid=False,
            reason=(
                f'duplicate foreign key "{foreign_key}" defined on a primary key '
                f'property "{property_name}" already defined on the property '
                f'"{seen_on_property_name}" on the schema "{name}" that implements an '
                "association table for the many-to-many relationship property "
                f'"{association.property.name}" on the schema '
                f'"{association.parent.name}"'
            ),
        )

    return types.Result(valid=True, reason=None)


def _check_properties_valid(
    name: str,
    schema: oa_types.Schema,
    association: association_helper.TParentPropertySchema,
    schemas: oa_types.Schemas,
) -> types.Result:
    """
    Check that all primary key properties are valid.

    Assume that all primary keys define a foreign key.

    Check that:
    1. the primary keys have one of the expected foreign keys,
    2. that the primary key type matches and
    3. that the format, maxLength match the expectation, including whether they should
        be defined.

    Args:
        name: The name of the schema.
        schema: The schema to validate.
        association: Information about the association property.
        schemas: All defined schemas.

    Returns:
        Whether the schema is valid with a reason if it is not.

    """
    # Calculate the expected schema
    expected_schema = association_helper.calculate_schema(
        property_schema=association.property.schema,
        parent_schema=association.parent.schema,
        schemas=schemas,
    ).schema
    # Creating a mapping of foreign key to expected property schema
    expected_foreign_key_properties = {
        property_[oa_types.ExtensionProperties.FOREIGN_KEY]: property_
        for property_ in expected_schema[oa_types.OpenApiProperties.PROPERTIES].values()
    }

    # Check primary keys
    primary_key_properties = _primary_key_property_items_iterator(schema, schemas)
    for property_name, property_schema in primary_key_properties:
        property_foreign_key = peek.prefer_local(
            get_value=peek.foreign_key,
            schema=property_schema,
            schemas=schemas,
        )

        # Check that the foreign key is expected
        if property_foreign_key not in expected_foreign_key_properties:
            expected_foreign_keys = ", ".join(
                map(lambda key: f'"{key}"', expected_foreign_key_properties.keys())
            )
            return types.Result(
                valid=False,
                reason=(
                    f'unexpected foreign key "{property_foreign_key}" defined on a '
                    f'primary key property "{property_name}" on the schema "{name}" '
                    "that implements an association table for the many-to-many "
                    f'relationship property "{association.property.name}" on the '
                    f'schema "{association.parent.name}", expected one of '
                    f"{expected_foreign_keys}"
                ),
            )

        # Check that the property schema is as expected
        expected_schema = expected_foreign_key_properties[property_foreign_key]
        checks = (
            (oa_types.OpenApiProperties.TYPE, peek.type_),
            (oa_types.OpenApiProperties.FORMAT, peek.format_),
            (oa_types.OpenApiProperties.MAX_LENGTH, peek.max_length),
        )
        for key, func in checks:
            # Check that values match
            result = value.check_matches(
                func=func,
                reference_schema=expected_schema,
                check_schema=property_schema,
                schemas=schemas,
            )
            if result is None:
                continue

            return types.Result(
                valid=False,
                reason=(
                    f"unexpected {key} ({result}) defined on a "
                    f'primary key property "{property_name}" on the schema "{name}" '
                    "that implements an association table for the many-to-many "
                    f'relationship property "{association.property.name}" on the '
                    f'schema "{association.parent.name}"'
                ),
            )

    return types.Result(valid=True, reason=None)


def _validate_schema(
    name: str,
    schema: oa_types.Schema,
    association: association_helper.TParentPropertySchema,
    schemas: oa_types.Schemas,
) -> types.Result:
    """
    Validate the schema for an association against the expected schema.

    Assume that schemas are individually valid.

    A know limitation is that the following invalid schema would pass:
    Parent:
        x-tablename: parent
    Child1:
        allOf:
            -   $ref: "#/components/schemas/Parent"
            -   properties:
                    x-inherits: true
                    prop_1:
                        primary_key: true
                        x-foreign-key: foreign.key
    Child2:
        allOf:
            -   $ref: "#/components/schemas/Parent"
            -   properties:
                    x-inherits: true
                    prop_2:
                        primary_key: true
                        x-foreign-key: foreign.key
    The problem is that both Child1 and Child2 define the same foreign key but are
    different schemas. Schemas are considered in isolation.

    Args:
        name: The name of the schema.
        schema: The schema to validate.
        association: The information about the many-to-many property.
        schemas: All defined schemas.

    """
    checks = [
        _check_2_or_fewer_primary_key,
        _check_primary_key_no_foreign_key,
        _check_duplicate_foreign_key,
        _check_properties_valid,
    ]
    for validation_check in checks:
        result = validation_check(name, schema, association, schemas)
        if not result.valid:
            return result

    return types.Result(valid=True, reason=None)


def check(*, schemas: oa_types.Schemas) -> types.Result:
    """
    Check that any schemas that implement association tables are valid.

    Assume that schemas are otherwise valid.

    The algorithm is:
    1. get a mapping of x-secondary to property information,
    2. iterate over schemas and retrieve all that have define an association and
    3. validate those schemas.

    Args:
        schemas: The schemas to check.

    Returns:
        Whether the schemas that define association tables are valid.

    """
    # Get mapping
    secondary_parent_property_schema_mapping = (
        association_helper.get_secondary_parent_property_schema_mapping(schemas=schemas)
    )

    # Get association schemas
    association_schemas = _get_defined_association_iterator(
        schemas, secondary_parent_property_schema_mapping
    )

    # Validate schemas
    for association_schema in association_schemas:
        association_info = secondary_parent_property_schema_mapping[
            association_schema.tablename
        ]
        result = _validate_schema(
            association_schema.name,
            association_schema.schema,
            association_info,
            schemas,
        )
        if not result.valid:
            return result

    return types.Result(valid=True, reason=None)
