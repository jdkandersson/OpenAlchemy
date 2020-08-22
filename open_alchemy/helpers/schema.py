"""Helpers for schemas."""

import typing

from .. import exceptions
from .. import types
from . import all_of as all_of_helper
from . import peek
from . import ref as ref_helper


def constructable(*, schema: types.Schema, schemas: types.Schemas) -> bool:
    """
    Check that a schema is constructable.

    The rules are:
    1. the resolved schema must have either x-tablename or x-inherits and
    2. the schema cannot just be a local $ref.

    Args:
        schema: The schema to check.

    Returns:
        Whether the schema is constructable.

    """
    if not isinstance(schema, dict):
        return False
    # Check for reference only models
    ref = schema.get("$ref")
    if ref is not None and (not isinstance(ref, str) or ref.startswith("#")):
        return False
    # Check allOf
    all_of = schema.get("allOf")
    if all_of is not None and (not isinstance(all_of, list) or len(all_of) < 2):
        if not isinstance(all_of, list) or not all_of:
            return False
        return constructable(schema=all_of[0], schemas=schemas)
    # Check for tablename and inherits
    tablename = peek.peek_key(schema=schema, schemas=schemas, key="x-tablename")
    try:
        schema_inherits = inherits(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return True
    return tablename is not None or schema_inherits is True


def inherits(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Check whether a schema inherits.

    Args:
        schema: The schema to check.
        schemas: All the schemas.

    Returns:
        Whether the schema inherits.

    """
    inherits_value = peek.inherits(schema=schema, schemas=schemas)
    if inherits_value is None:
        return None
    if isinstance(inherits_value, str) or inherits_value is True:
        return True
    return False


def prepare(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    skip_name: typing.Optional[str] = None,
) -> types.Schema:
    """
    Resolve $ref and merge allOf.

    Args:
        schema: The schema to prepare.
        schemas: The schemas from which to resolve any $ref.
        skip_name (optional): Any schema name to skip.

    Returns:
        The prepared schema.

    """
    _, schema = ref_helper.resolve(
        name="", schema=schema, schemas=schemas, skip_name=skip_name
    )
    return all_of_helper.merge(schema=schema, schemas=schemas, skip_name=skip_name)


def prepare_deep(schema: types.Schema, schemas: types.Schemas):
    """
    Resolve $ref and merge allOf including for object properties and items.

    Assume the schema is a valid JSONSchema.

    Args:
        schema: The schema to prepare.
        schemas: The schemas from which to resolve any $ref.

    Returns:
        The prepared schema.

    """
    schema = prepare(schema=schema, schemas=schemas)

    # Resolve $ref in any properties
    properties = schema.get("properties", None)
    if properties is not None:
        for name, prop_schema in properties.items():
            properties[name] = prepare_deep(schema=prop_schema, schemas=schemas)

    # Resolve $ref of any items
    items_schema = schema.get("items", None)
    if items_schema is not None:
        schema["items"] = prepare_deep(schema=items_schema, schemas=schemas)

    return schema
