"""Used to resolve schema references."""

import re

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


def resolve_ref(*, schema: types.Schema, schemas: types.Schemas):
    """Resolve $ref schemas to the underlying schema."""
    # Checking whether schema is a reference schema
    ref = schema.get("$ref")
    if ref is None:
        return schema

    # Checking value of $ref
    match = _REF_PATTER.match(ref)
    if not match:
        raise exceptions.SchemaNotFoundError(
            f"{ref} format incorrect, expected #/components/schemas/<SchemaName>"
        )

    print(schemas)
    return schema
