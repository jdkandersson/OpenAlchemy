"""Functions to expose iterables for schemas."""

import typing

from ... import helpers
from ... import types


def constructable(
    *, schemas: types.Schemas
) -> typing.Iterator[typing.Tuple[str, types.Schema]]:
    """
    Create an iterable with all constructable schemas from all schemas.

    Iterates over all items in the schemas, checks whether a schema is constructable and
    yields those that are.

    Args:
        schemas: The schemas to iterate over.

    Returns:
        iterable with all schemas that are constructable.

    """
    for name, schema in schemas.items():
        if not helpers.schema.constructable(schema=schema, schemas=schemas):
            continue

        yield name, schema


def properties(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Iterator[typing.Tuple[str, types.Schema]]:
    """
    Create an iterable with all properties of a schema from a constructable schema.

    Checks for $ref, if it is there resolves to the underlying schema and recursively
    processes that schema.
    Checks for allOf, if it is there recursively processes each schema.
    Otherwise looks for properties and yields all items if the key exists.

    Args:
        schema: The constructable schems.
        schemas: All defined schemas (not just the constructable ones).

    Returns:
        An interator with all properties of a schema.

    """
    # Handle $ref
    if schema.get("$ref") is not None:
        _, ref_schema = helpers.ref.resolve(name="", schema=schema, schemas=schemas)
        yield from properties(schema=ref_schema, schemas=schemas)

    # Handle allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        for sub_schema in all_of:
            yield from properties(schema=sub_schema, schemas=schemas)

    # Handle simple case
    schema_properties = schema.get("properties")
    if schema_properties is None:
        return
    yield from schema_properties.items()
