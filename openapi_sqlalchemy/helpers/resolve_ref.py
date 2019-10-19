"""Used to resolve schema references."""

import re
import typing

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


def resolve_ref(
    *,
    name: str,
    schema: typing.Dict[str, typing.Any],
    schemas: typing.Dict[str, typing.Dict[str, typing.Any]],
) -> typing.Tuple[str, types.SchemaSpec]:
    """
    Resolve reference to another schema.

    Recursively resolves $ref until $ref key is no longer found. On each step, the name
    of the schema is recorded.

    Raises SchemaNotFound is a $ref resolution fails.

    Args:
        name: The name of the schema from the last step.
        schema: The specification of the schema from the last step.
        schemas: Dictionary with all defined schemas used to resolve $ref.

    Returns:
        The first schema that no longer has the $ref key and the name of that schema.

    """
    # Checking whether schema is a reference schema
    ref = schema.get("$ref")
    if ref is None:
        return name, schema

    # Checking value of $ref
    match = _REF_PATTER.match(ref)
    if not match:
        raise exceptions.SchemaNotFoundError(
            f"{ref} format incorrect, expected #/components/schemas/<SchemaName>"
        )

    # Retrieving new schema
    ref_name = match.group(1)
    ref_schema = schemas.get(ref_name)
    if ref_schema is None:
        raise exceptions.SchemaNotFoundError(f"{ref_name} was not found in schemas.")

    return resolve_ref(name=ref_name, schema=ref_schema, schemas=schemas)
