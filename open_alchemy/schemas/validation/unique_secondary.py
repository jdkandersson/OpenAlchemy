"""Check that all x-secondary are unique."""

import typing

from ... import types as oa_types
from ...helpers import relationship
from ..helpers import association as association_helper
from ..helpers import iterate
from . import types


class _TSeenSecondary(typing.NamedTuple):
    """Records information about the secondary that has been seen."""

    schema_name: str
    property_name: str


def check(*, schemas: oa_types.Schemas) -> types.Result:
    """
    Check that all x-secondary are unique.

    Assume that schemas are otherwise valid.

    The algorithm is:
    1. iterate over constructable schemas,
    2. iterate over properties restricted to model context,
    3. filter for many-to-many relationship properties,
    3. record the secondary, property and schema name,
    4. if a secondary has already been seen, return result that is not valid and
    5. return valid result.

    Args:
        schemas: The schemas to check.

    Returns:
        Whether the schemas have unique secondary values and the reason if not.

    """
    constructable_schemas = iterate.constructable(schemas=schemas)

    # Track information about the x-secondary values that are encountered
    seen_secondaries: typing.Dict[str, _TSeenSecondary] = {}

    for schema_name, schema in constructable_schemas:
        properties = iterate.properties_items(
            schema=schema, schemas=schemas, stay_within_model=True
        )

        for property_name, property_schema in properties:
            # Skip properties that are not many-to-many relationships
            is_many_to_many = relationship.is_relationship_type(
                type_=oa_types.RelationshipType.MANY_TO_MANY,
                schema=property_schema,
                schemas=schemas,
            )
            if not is_many_to_many:
                continue

            # Retrieve secondary value
            secondary = association_helper.get_secondary(
                schema=property_schema, schemas=schemas
            )

            # Check whether secondary has already been seen
            if secondary not in seen_secondaries:
                seen_secondaries[secondary] = _TSeenSecondary(
                    schema_name=schema_name, property_name=property_name
                )
                continue

            # Construct reason that schemas are not valid
            seen_on_schema = seen_secondaries[secondary]
            return types.Result(
                valid=False,
                reason=(
                    f'duplicate "x-secondary value {secondary} defined on the property '
                    f"{property_name} on the schema {schema_name} has already been "
                    f"defined on the property {seen_on_schema.property_name} on the "
                    f"schema {seen_on_schema.schema_name}"
                ),
            )

    return types.Result(valid=True, reason=None)
