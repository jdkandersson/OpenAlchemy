"""Pre-process schemas by adding any association tables as a schema to schemas."""

from .. import types
from . import helpers


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
    association_properties = helpers.association.get_association_property_iterator(
        schemas=schemas
    )
    association_schemas = list(
        map(
            lambda args: helpers.association.calculate_schema(
                property_schema=args.property_.schema,
                parent_schema=args.parent.schema,
                schemas=schemas,
            ),
            association_properties,
        )
    )
    for association in association_schemas:
        schemas[association.name] = association.schema
