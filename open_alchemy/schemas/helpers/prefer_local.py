"""Retrieve the value of a key preferably without following a $ref."""

import typing

from ... import types


class PeekValue(types.Protocol):
    """Defines interface for peek functions."""

    def __call__(self, *, schema: types.Schema, schemas: types.Schemas) -> typing.Any:
        """Call signature for peek functions."""
        ...


def get(
    *, get_value: PeekValue, schema: types.Schema, schemas: types.Schemas
) -> typing.Any:
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

        def map_to_value(sub_schema: types.Schema) -> typing.Any:
            """Use get_value to turn the schema into the value."""
            return get_value(schema=sub_schema, schemas=schemas)

        retrieved_values = map(map_to_value, no_ref)
        not_none_retrieved_values = filter(
            lambda value: value is not None, retrieved_values
        )
        retrieved_value = next(not_none_retrieved_values, None)
        if retrieved_value is not None:
            return retrieved_value
    return get_value(schema=schema, schemas=schemas)
