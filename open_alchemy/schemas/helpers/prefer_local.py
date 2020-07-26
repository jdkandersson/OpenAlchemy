"""Retrieve the value of a key preferably without following a $ref."""

from ... import helpers
from ... import types


def get(
    *, get_value: helpers.peek.PeekValue, schema: types.Schema, schemas: types.Schemas
) -> helpers.peek.PeekValueT:
    """
    Retrieve the value using a function preferably without having to follow a $ref.

    1. Check for allOf:
        if found, iterate over schemas in allOf and skip any that contain $ref and
            return the value returned by get_value if it is not None.
    2. Return output of get_value called on the schema.

    Args:
        get_value: The function that knows how to retrieve the value.
        schema: The schema to process.
        schemas: All the schemas.

    Returns:
        The value returned by get_value preferably without following any $ref.

    """
    all_of = schema.get("allOf")
    if all_of is not None:
        no_ref = filter(lambda sub_schema: sub_schema.get("$ref") is None, all_of)

        def map_to_value(sub_schema: types.Schema) -> helpers.peek.PeekValueT:
            """Use get_value to turn the schema into the value."""
            return get_value(schema=sub_schema, schemas=schemas)

        retrieved_values = map(map_to_value, no_ref)
        retrieved_value = next(
            (value for value in retrieved_values if value is not None), None
        )
        if retrieved_value is not None:
            return retrieved_value
    return get_value(schema=schema, schemas=schemas)
