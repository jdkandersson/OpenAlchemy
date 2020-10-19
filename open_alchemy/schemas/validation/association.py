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
    primary_key_properties = _primary_key_property_items_iterator(
        schema=schema, schemas=schemas
    )
    for property_name, property_schema in primary_key_properties:
        # Check for foreign key
        foreign_key = oa_helpers.peek.foreign_key(
            schema=property_schema, schemas=schemas
        )
        if foreign_key:
            continue

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
