"""Used to resolve schema references."""

import re

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


def resolve_ref(*, schema: types.Schema, schemas: types.Schemas) -> types.Schema:
    """
    Resolve $ref schemas to the underlying schema.

    Args:
        schema: The schema to operate on.
        schemas: All the schemas used to resolve referenced schemas.

    Returns:
        The schema where all top level $ref have been removed.

    """
    # Checking whether schema is a reference schema
    ref = schema.spec.get("$ref")
    if ref is None:
        return schema

    # Checking value of $ref
    match = _REF_PATTER.match(ref)
    if not match:
        raise exceptions.SchemaNotFoundError(
            f"{ref} format incorrect, expected #/components/schemas/<SchemaName>"
        )

    # Retrieving new schema
    schema_name = match.group(1)
    ref_schema = schemas.get(schema_name)
    if ref_schema is None:
        raise exceptions.SchemaNotFoundError(f"{schema_name} was not found in schemas.")

    new_schema = types.Schema(schema_name, ref_schema)
    return resolve_ref(schema=new_schema, schemas=schemas)
