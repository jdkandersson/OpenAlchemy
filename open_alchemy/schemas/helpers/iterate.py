"""Functions to expose iterables for schemas."""

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
    stay_within_tablename: bool = False,
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
        stay_within_tablename: Ensures that on properties on the same table are
            iterated over. For joined table inheritance, the reference to the parent is
            not followed.
        stay_within_model: Ensures that each property is only returned once. For both
            single and joined table inheritance no reference to the parent is followed.

    Returns:
        An interator with all properties of a schema.

    """
    skip_name: typing.Optional[str] = None
    if stay_within_tablename or stay_within_model:
        try:
            inheritance_type = helpers.inheritance.calculate_type(
                schema=schema, schemas=schemas
            )
            if inheritance_type != helpers.inheritance.Type.NONE:
                parent_name = helpers.inheritance.retrieve_parent(
                    schema=schema, schemas=schemas
                )

                # Check for single
                if stay_within_model:
                    skip_name = parent_name

                # Check for JOINED
                if (
                    not stay_within_model
                    and inheritance_type == helpers.inheritance.Type.JOINED_TABLE
                    and stay_within_tablename
                ):
                    skip_name = parent_name
        except (
            exceptions.MalformedSchemaError,
            exceptions.InheritanceError,
            exceptions.SchemaNotFoundError,
        ):
            return

    yield from _properties(schema=schema, schemas=schemas, skip_name=skip_name)


def _properties(
    *, schema: types.Schema, schemas: types.Schemas, skip_name: typing.Optional[str],
) -> typing.Iterator[typing.Tuple[str, types.Schema]]:
    """Private interface for properties."""
    if not isinstance(schema, dict):
        return

    # Handle $ref
    if schema.get("$ref") is not None:
        try:
            _, ref_schema = helpers.ref.resolve(
                name="", schema=schema, schemas=schemas, skip_name=skip_name
            )
        except (exceptions.MalformedSchemaError, exceptions.SchemaNotFoundError):
            return
        yield from _properties(schema=ref_schema, schemas=schemas, skip_name=skip_name)

    # Handle allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        if not isinstance(all_of, list):
            return
        for sub_schema in all_of:
            yield from _properties(
                schema=sub_schema, schemas=schemas, skip_name=skip_name
            )

    # Handle simple case
    schema_properties = schema.get("properties")
    if not isinstance(schema_properties, dict):
        return
    yield from schema_properties.items()
