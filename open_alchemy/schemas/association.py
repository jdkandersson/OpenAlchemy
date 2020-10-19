"""Pre-process schemas by adding any association tables as a schema to schemas."""

import functools
import typing

from .. import helpers as oa_helpers
from .. import types
from . import helpers


def _requires_association(schemas: types.Schemas, schema: types.Schema) -> bool:
    """
    Calculate whether a property requires an association table.

    Args:
        schema: The schema of the property to check.

    Returns:
        Whether the property requires an association table.

    """
    return oa_helpers.relationship.is_relationship_type(
        type_=oa_helpers.relationship.Type.MANY_TO_MANY, schema=schema, schemas=schemas
    )


def _get_association_property_iterator(
    *, schemas: types.Schemas
) -> typing.Iterable[typing.Tuple[types.Schemas, types.Schema, types.Schema]]:
    """
    Get an iterator for properties that require association tables from the schemas.

    To ensure no duplication, property iteration stays within the model context.

    Args:
        schemas: All defined schemas.

    Returns:
        An iterator with properties that require an association table along with the
        schemas and the parent schema.

    """
    constructables = helpers.iterate.constructable(schemas=schemas)
    constructable_schemas = map(lambda args: args[1], constructables)
    for schema in constructable_schemas:
        properties = helpers.iterate.properties_items(
            schema=schema, schemas=schemas, stay_within_model=True
        )
        property_schemas = map(lambda args: args[1], properties)
        association_property_schemas = filter(
            functools.partial(_requires_association, schemas), property_schemas
        )
        yield from (
            (schemas, schema, property_) for property_ in association_property_schemas
        )


def process(*, schemas: types.Schemas) -> None:
    """
    Pre-process the schemas to add association schemas as necessary.

    Algorithm:
    1. Iterate over all schemas and their properties retaining the parent schema and the
        schemas in the context and staying within the model properties only
    2. Filter for properties that (1) are relationships and (2) are many-to-many
        relationships
    3. Convert the property schema to an association schema
    4. Add them to the schemas

    Args:
        schemas: The schemas to process.

    """
    association_properties = _get_association_property_iterator(schemas=schemas)
    association_schemas = list(
        map(
            lambda args: helpers.association.calculate_schema(
                property_schema=args[2], parent_schema=args[1], schemas=args[0]
            ),
            association_properties,
        )
    )
    for association in association_schemas:
        schemas[association.name] = association.schema
