"""Validate association tables."""

import typing

from ... import helpers as oa_helpers
from ... import types as oa_types
from .. import helpers
from . import types


def _get_defined_association_iterator(
    *, schemas: oa_types.Schemas, tablename_mapping: typing.Dict[str, typing.Any]
) -> typing.Iterable[typing.Tuple[str, oa_types.Schema]]:
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
    constructables = helpers.iterate.constructable(schemas=schemas)
    return filter(
        lambda args: oa_helpers.peek.tablename(schema=args[1], schemas=schemas)
        in tablename_mapping,
        constructables,
    )


def _primary_key_property_items_iterator(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> typing.Iterator[typing.Tuple[str, oa_types.Schema]]:
    """
    Get an iterable with only primary key properties.

    Args:
        schema: The schema to get primary key properties from.
        schemas: All defined schemas.

    Returns:
        An iterator with all primary key properties.

    """
    properties = helpers.iterate.properties_items(schema=schema, schemas=schemas)
    return filter(
        lambda args: oa_helpers.peek.prefer_local(
            get_value=oa_helpers.peek.primary_key,
            schema=args[1],
            schemas=schemas,
        ),
        properties,
    )


def _check_2_or_fewer_primary_key(
    *,
    name: str,
    schema: oa_types.Schema,
    association: helpers.association.TParentPropertySchema,
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
    primary_key_properties = _primary_key_property_items_iterator(
        schema=schema, schemas=schemas
    )
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
    *,
    name: str,
    schema: oa_types.Schema,
    association: helpers.association.TParentPropertySchema,
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
    primary_key_properties = _primary_key_property_items_iterator(
        schema=schema, schemas=schemas
    )
    not_foreign_key_primary_key_properties = filter(
        lambda args: oa_helpers.peek.foreign_key(schema=args[1], schemas=schemas)
        is None,
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
    *,
    name: str,
    schema: oa_types.Schema,
    association: helpers.association.TParentPropertySchema,
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
    primary_key_properties = _primary_key_property_items_iterator(
        schema=schema, schemas=schemas
    )
    foreign_keys = map(
        lambda args: (
            args[0],
            oa_helpers.peek.prefer_local(
                get_value=oa_helpers.peek.foreign_key, schema=args[1], schemas=schemas
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


# def _check_properties_valid(
#     *,
#     name: str,
#     schema: oa_types.Schema,
#     association: helpers.association.TParentPropertySchema,
#     schemas: oa_types.Schemas,
# ) -> types.Result:
#     """
#     Check that all primary key properties are valid.

#     Assume that all primary keys define a foreign key.

#     Check that:
#     1. the primary keys have one of the expected foreign keys,
#     2. that the primary key type matches and
#     3. that the format, maxLength match the expectation, including whether they should
#         be defined.

#     Args:
#         name: The name of the schema.
#         schema: The schema to validate.
#         association: Information about the association property.
#         schemas: All defined schemas.

#     Returns:
#         Whether the schema is valid with a reason if it is not.

#     """


# def validate_schema(
#     *,
#     name: str,
#     schema: oa_types.Schema,
#     association: helpers.association.TParentPropertySchema,
#     schemas: oa_types.Schemas,
# ) -> types.Result:
#     """
#     Validate the schema for an association against the expected schema.

#     Assume that schemas are individually valid.

#     Args:
#         name: The name of the schema.
#         schema: The schema to validate.
#         association: The information about the many-to-many property.
#         schemas: All defined schemas.

#     """
