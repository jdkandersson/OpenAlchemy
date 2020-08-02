"""Functions to expose iterables for schemas."""

# pylint: disable=unused-argument

import typing

from ... import exceptions
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
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    stay_within_tablename_scope: bool = False,
    stay_within_model: bool = False,
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
        stay_within_tablename_scope: Ensures that on properties on the same table are
            iterated over. For joined table inheritance, the reference to the parent is
            not followed.
        stay_within_model: Ensures that each property is only returned once. For both
            single and joined table inheritance no reference to the parent is followed.

    Returns:
        An interator with all properties of a schema.

    """
    if not isinstance(schema, dict):
        return

    # Handle $ref
    if schema.get("$ref") is not None:
        try:
            _, ref_schema = helpers.ref.resolve(name="", schema=schema, schemas=schemas)
        except (exceptions.MalformedSchemaError, exceptions.SchemaNotFoundError):
            return
        yield from properties(schema=ref_schema, schemas=schemas)

    # Handle allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        if not isinstance(all_of, list):
            return
        for sub_schema in all_of:
            yield from properties(schema=sub_schema, schemas=schemas)

    # Handle simple case
    schema_properties = schema.get("properties")
    if schema_properties is None:
        return
    yield from schema_properties.items()
