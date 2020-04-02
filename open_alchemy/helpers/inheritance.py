"""Helpers to support inheritance."""

import typing

from .. import exceptions
from .. import types
from . import ref as ref_helper
from . import schema as schema_helper


def check_parent(
    *, schema: types.Schema, parent_name: str, schemas: types.Schemas
) -> bool:
    """External interface."""
    return _check_parent(schema, parent_name, schemas)


def _check_parent(
    schema: types.Schema,
    parent_name: str,
    schemas: types.Schemas,
    seen_refs: typing.Optional[typing.Set[str]] = None,
) -> bool:
    """
    Check that the parent is in the inheritance chain of a schema.

    Recursive function. The base cases are:
    1. the schema has $ref where the name matches the parent name if
        a. the referenced schema is constructable, return True or
        b. if the referenced schema is not constructable, return False and
    2. the schema does not have $ref nor allOf in which case return False.

    The recursive cases are:
    1. the schema has $ref where the name does not match the parent name in which case
        the function is called with the referenced schema and
    2. the schema has allOf where the function is called on each element in allOf and,
        if True is returned for any of them, True is returned otherwise False is
        returned.

    Raise MalformedSchemaError if the parent is not found in the chain.
    Raise MalformedSchemaError if the parent does not have x-tablename nor x-inherits.

    Args:
        schema: The schema to check.
        parent_name: The parent to check for in the inheritance chain.
        schemas: All the schemas.
        seen_refs: The $ref that have already been check to avoid circular dependencies.

    Returns:
        Whether the parent is in the inheritance chain.

    """
    if seen_refs is None:
        seen_refs = set()

    # Check for $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")
    if ref is None and all_of is None:
        return False

    # Handle $ref
    if ref is not None:
        if not isinstance(ref, str):
            raise exceptions.MalformedSchemaError("The value of $ref must be a string.")

        # Check for circular references
        if ref in seen_refs:
            raise exceptions.MalformedSchemaError(
                "Circular reference chain detected for the schema."
            )
        seen_refs.add(ref)

        ref_name, ref_schema = ref_helper.get_ref(ref=ref, schemas=schemas)

        # Check for name match base case
        if ref_name == parent_name:
            return schema_helper.constructable(schema=ref_schema, schemas=schemas)

        # Recursive case
        return _check_parent(ref_schema, parent_name, schemas, seen_refs)

    # Handle allOf
    if not isinstance(all_of, list):
        raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
    return any(
        _check_parent(sub_schema, parent_name, schemas, seen_refs)
        for sub_schema in all_of
    )


def get_parent(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """External interface."""
    return _get_parent(schema, schemas)


def _get_parent(
    schema: types.Schema,
    schemas: types.Schemas,
    seen_refs: typing.Optional[typing.Set[str]] = None,
) -> str:
    """
    Get the name of the parent of the schema.

    Recursive function. The base cases are:
    1. the schema has $ref and the referenced schema is constructable.

    The recursive cases are:
    1. the schema has $ref where the referenced schema is not constructable in which
        case the function is called with the referenced schema and
    2. the schema has allOf in which case the return value of the first element that
        does not raise the MalformedSchemaError is returned.

    Raise MalformedSchemaError if the schema does not have $ref nor allOf.
    Raise MalformedSchemaError if the schema has allOf and all of the elements raise
        MalformedSchemaError.

    Args:
        schema: The schema to retrieve the parent for.
        schemas: All the schemas.
        seen_refs: The $ref that have already been check to avoid circular dependencies.

    Returns:
        The name of the parent.

    """
    if seen_refs is None:
        seen_refs = set()

    # Check for $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")
    if ref is None and all_of is None:
        raise exceptions.MalformedSchemaError(
            "A schema that is marked as inhereting does not reference a valid parent."
        )

    # Handle $ref
    if ref is not None:
        if not isinstance(ref, str):
            raise exceptions.MalformedSchemaError("The value of $ref must be a string.")

        # Check for circular references
        if ref in seen_refs:
            raise exceptions.MalformedSchemaError(
                "Circular reference chain detected for the schema."
            )
        seen_refs.add(ref)

        ref_name, ref_schema = ref_helper.get_ref(ref=ref, schemas=schemas)

        # Check whether the referenced schema is constructible
        if schema_helper.constructable(schema=ref_schema, schemas=schemas):
            return ref_name

        # Recursive case
        return _get_parent(ref_schema, schemas, seen_refs)

    # Handle allOf
    if not isinstance(all_of, list):
        raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
    # Find first constructable schema
    for sub_schema in all_of:
        try:
            return _get_parent(sub_schema, schemas, seen_refs)
        except exceptions.MalformedSchemaError:
            pass
    # None of the schemas in allOf are constructable
    raise exceptions.MalformedSchemaError(
        "A schema that is marked as inhereting does not reference a valid parent."
    )
