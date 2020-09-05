"""Functions to expose iterables for schemas."""

import functools
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
        try:
            if not helpers.schema.constructable(schema=schema, schemas=schemas):
                continue
        except (exceptions.MalformedSchemaError, exceptions.SchemaNotFoundError):
            continue

        yield name, schema


def not_constructable(
    *, schemas: types.Schemas
) -> typing.Iterator[typing.Tuple[str, types.Schema]]:
    """
    Create an iterable with all non-constructable schemas from all schemas.

    Iterates over all items in the schemas, checks whether a schema is not constructable
    and yields those that are.

    Args:
        schemas: The schemas to iterate over.

    Returns:
        iterable with all schemas that are not constructable.

    """
    for name, schema in schemas.items():
        try:
            if helpers.schema.constructable(schema=schema, schemas=schemas):
                continue
        except (exceptions.MalformedSchemaError, exceptions.SchemaNotFoundError):
            continue

        yield name, schema


def _calculate_skip_name(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    stay_within_tablename: bool = False,
    stay_within_model: bool = False,
) -> typing.Optional[str]:
    """
    Calculate the references to skip depending on the inheritance.

    Args:
        schema: The constructable schems.
        schemas: All defined schemas (not just the constructable ones).
        stay_within_tablename: Ensures that on properties on the same table are
            iterated over. For joined table inheritance, the reference to the parent is
            not followed.
        stay_within_model: Ensures that each property is only returned once. For both
            single and joined table inheritance no reference to the parent is followed.

    Returns:
        The references to skip or None.

    """
    if not stay_within_tablename and not stay_within_model:
        return None

    inheritance_type = helpers.inheritance.calculate_type(
        schema=schema, schemas=schemas
    )
    if inheritance_type != helpers.inheritance.Type.NONE:
        parent_name = helpers.inheritance.retrieve_parent(
            schema=schema, schemas=schemas
        )

        # Check for single
        if stay_within_model:
            return parent_name

        # Check for JOINED
        if (
            not stay_within_model
            and inheritance_type == helpers.inheritance.Type.JOINED_TABLE
            and stay_within_tablename
        ):
            return parent_name

    return None


def _filter_duplicates(seen_keys: typing.Set[str], args) -> bool:
    """Remove duplicate values."""
    key, _ = args

    if key in seen_keys:
        return False

    seen_keys.add(key)
    return True


def properties_items(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    stay_within_tablename: bool = False,
    stay_within_model: bool = False,
) -> typing.Iterator[typing.Any]:
    """
    Create an iterable with all properties of a schema from a constructable schema.

    Checks for $ref, if it is there resolves to the underlying schema and recursively
    processes that schema.
    Checks for allOf, if it is there recursively processes each schema.
    Otherwise looks for properties and yields all items if the key exists.

    Args:
        schema: The constructable schems.
        schemas: All defined schemas (not just the constructable ones).
        stay_within_tablename: Ensures that only properties on the same table are
            iterated over. For joined table inheritance, the reference to the parent is
            not followed.
        stay_within_model: Ensures that each property is only returned once. For both
            single and joined table inheritance no reference to the parent is followed.

    Returns:
        An iterator with all properties of a schema.

    """
    init_filter_duplicates = functools.partial(_filter_duplicates, set())

    properties_values_iterator = properties_values(
        schema=schema,
        schemas=schemas,
        stay_within_tablename=stay_within_tablename,
        stay_within_model=stay_within_model,
    )
    for properties_value in properties_values_iterator:
        if not isinstance(properties_value, dict):
            continue
        yield from filter(init_filter_duplicates, properties_value.items())


def properties_values(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    stay_within_tablename: bool = False,
    stay_within_model: bool = False,
) -> typing.Iterator[typing.Any]:
    """
    Return iterable with all values of the properties key of the constructable schema.

    Checks for $ref, if it is there resolves to the underlying schema and recursively
    processes that schema.
    Checks for allOf, if it is there recursively processes each schema.
    Otherwise yields the properties key value.

    Args:
        schema: The constructable schems.
        schemas: All defined schemas (not just the constructable ones).
        stay_within_tablename: Ensures that only properties on the same table are
            iterated over. For joined table inheritance, the reference to the parent is
            not followed.
        stay_within_model: Ensures that each properties value is only returned once. For
            both single and joined table inheritance no reference to the parent is
            followed.

    Returns:
        An iterator with all properties key values.

    """
    skip_name: typing.Optional[str] = None
    try:
        skip_name = _calculate_skip_name(
            schema=schema,
            schemas=schemas,
            stay_within_tablename=stay_within_tablename,
            stay_within_model=stay_within_model,
        )
    except (
        exceptions.MalformedSchemaError,
        exceptions.InheritanceError,
        exceptions.SchemaNotFoundError,
    ):
        return

    yield from _any_key(
        schema=schema, schemas=schemas, skip_name=skip_name, key="properties"
    )


def _any_key(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    skip_name: typing.Optional[str],
    key: str,
) -> typing.Iterator[typing.Any]:
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
        yield from _any_key(
            schema=ref_schema, schemas=schemas, skip_name=skip_name, key=key
        )

    # Handle allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        if not isinstance(all_of, list):
            return

        all_of_dicts = list(
            filter(lambda sub_schema: isinstance(sub_schema, dict), all_of)
        )

        # Process not $ref first
        all_of_no_ref = filter(
            lambda sub_schema: not helpers.peek.peek_key(
                schema=sub_schema, schemas=schemas, key="$ref"
            ),
            all_of_dicts,
        )
        for sub_schema in all_of_no_ref:
            yield from _any_key(
                schema=sub_schema, schemas=schemas, skip_name=skip_name, key=key
            )

        # Process $ref
        all_of_ref = filter(
            lambda sub_schema: helpers.peek.peek_key(
                schema=sub_schema, schemas=schemas, key="$ref"
            ),
            all_of_dicts,
        )
        for sub_schema in all_of_ref:
            yield from _any_key(
                schema=sub_schema, schemas=schemas, skip_name=skip_name, key=key
            )

    # Handle simple case
    value = schema.get(key)
    if value is None:
        return
    yield value


def required_values(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    stay_within_model: bool = False,
) -> typing.Iterator[typing.Any]:
    """
    Return iterable with all values of the required key of the constructable schema.

    Checks for $ref, if it is there resolves to the underlying schema and recursively
    processes that schema.
    Checks for allOf, if it is there recursively processes each schema.
    Otherwise yields the required key value.

    Args:
        schema: The constructable schems.
        schemas: All defined schemas (not just the constructable ones).
        stay_within_model: Ensures that each required value is only returned once. For
            both single and joined table inheritance no reference to the parent is
            followed.

    Returns:
        An iterator with all required key values.

    """
    skip_name: typing.Optional[str] = None
    try:
        skip_name = _calculate_skip_name(
            schema=schema,
            schemas=schemas,
            stay_within_tablename=False,
            stay_within_model=stay_within_model,
        )
    except (
        exceptions.MalformedSchemaError,
        exceptions.InheritanceError,
        exceptions.SchemaNotFoundError,
    ):
        return

    yield from _any_key(
        schema=schema, schemas=schemas, skip_name=skip_name, key="required"
    )


def required_items(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    stay_within_model: bool = False,
) -> typing.Iterator[typing.Any]:
    """
    Return iterable with all items of the required key of the constructable schema.

    Checks for $ref, if it is there resolves to the underlying schema and recursively
    processes that schema.
    Checks for allOf, if it is there recursively processes each schema.
    Otherwise yields the required key value.

    Args:
        schema: The constructable schems.
        schemas: All defined schemas (not just the constructable ones).
        stay_within_model: Ensures that each required value is only returned once. For
            both single and joined table inheritance no reference to the parent is
            followed.

    Returns:
        An iterator with all items of the required key.

    """
    required_values_iterator = required_values(
        schema=schema, schemas=schemas, stay_within_model=stay_within_model
    )
    for required_value in required_values_iterator:
        if not isinstance(required_value, list):
            continue
        yield from required_value


def backrefs_items(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
) -> typing.Iterator[typing.Any]:
    """
    Create an iterable with all backrefs of a schema from a constructable schema.

    Checks for $ref, if it is there resolves to the underlying schema and recursively
    processes that schema.
    Checks for allOf, if it is there recursively processes each schema.
    Otherwise looks for x-backrefs and yields all items if the key exists.

    Args:
        schema: The constructable schems.
        schemas: All defined schemas (not just the constructable ones).

    Returns:
        An iterator with all backrefs of a schema.

    """
    init_filter_duplicates = functools.partial(_filter_duplicates, set())

    backrefs_values_iterator = backrefs_values(
        schema=schema,
        schemas=schemas,
    )
    for backrefs_value in backrefs_values_iterator:
        if not isinstance(backrefs_value, dict):
            continue
        yield from filter(init_filter_duplicates, backrefs_value.items())


def backrefs_values(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
) -> typing.Iterator[typing.Any]:
    """
    Return iterable with all values of the backrefs key of the constructable schema.

    Checks for $ref, if it is there resolves to the underlying schema and recursively
    processes that schema.
    Checks for allOf, if it is there recursively processes each schema.
    Otherwise yields the backrefs key value.

    Args:
        schema: The constructable schems.
        schemas: All defined schemas (not just the constructable ones).

    Returns:
        An iterator with all backrefs key values.

    """
    yield from _any_key(
        schema=schema, schemas=schemas, skip_name=None, key="x-backrefs"
    )
