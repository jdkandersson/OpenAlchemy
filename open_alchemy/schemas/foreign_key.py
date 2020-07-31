"""Pre-processor that defines any foreign keys."""

from .. import exceptions
from .. import helpers
from .. import types


def _requires_foreign_key(schemas: types.Schemas, schema: types.Schema) -> bool:
    """
    Check whether the property requires a foreign key to be defined.

    Foreign keys are required for many-to-one, one-to-one and one-to-many relationships.
    The following rules capture this:
    1. not JSON,
    2. object or array type and
    3. no secondary table.

    Args:
        schemas: All the defined schemas used to resolve any $ref.
        schema: The schema of the property.

    Returns:
        Whether the property requires a foreign key.

    """
    # Check type
    try:
        type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    except exceptions.TypeMissingError:
        return False
    if type_ not in {"object", "array"}:
        return False

    # Map array
    if type_ == "array":
        items_schema = helpers.peek.items(schema=schema, schemas=schemas)
        if items_schema is None:
            return False
        schema = items_schema

    # Check json
    json = helpers.peek.json(schema=schema, schemas=schemas)
    if json is True:
        return False

    # Check secondary
    secondary = helpers.peek.secondary(schema=schema, schemas=schemas)
    if secondary is not None:
        return False

    return True