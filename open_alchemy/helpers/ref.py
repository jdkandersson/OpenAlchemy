"""Used to resolve schema references."""

import os
import re
import typing

from open_alchemy import exceptions
from open_alchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


NameSchema = typing.Tuple[str, types.Schema]


def resolve(*, name: str, schema: types.Schema, schemas: types.Schemas) -> NameSchema:
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

    ref_name, ref_schema = get_ref(ref=ref, schemas=schemas)

    return resolve(name=ref_name, schema=ref_schema, schemas=schemas)


def get_ref(*, ref: str, schemas: types.Schemas) -> NameSchema:
    """
    Get the schema referenced by ref.

    Raises SchemaNotFound is a $ref resolution fails.

    Args:
        ref: The reference to the schema.
        schemas: The schemas to use to resolve the ref.

    Returns:
        The schema referenced by ref.

    """
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

    return ref_name, ref_schema


def _add_remote_context(*, context: str, ref: str) -> str:
    """
    Add remote context to any $ref within a schema retrieved from a remote reference.

    There are 3 cases:
    1. The $ref value starts with # in which case the context is prepended.
    2. The $ref starts with a filename in which case only the file portion of the
        context is prepended.
    3. The $ref starts with a relative path and ends with a file in which case the file
        portion of the context is prepended and merged so that the shortest possible
        relative path is used.

    After the paths are merged the following operations are done:
    1. a normalized relative path is calculated (eg. turning ./dir1/../dir2 to ./dir2)
        and
    2. the case is normalized.

    Args:
        context: The context of the document from which the schema was retrieved which
            is the relative path to the file on the system from the base OpenAPI
            specification.
        ref: The value of a $ref within the schema.

    Returns:
        The $ref value with the context of the document included.

    """
    # Check reference value
    try:
        ref_context, ref_schema = ref.split("#")
    except ValueError:
        raise exceptions.MalformedSchemaError(
            f"A reference must contain exactly one #. Actual reference: {ref}"
        )
    context_head, _ = os.path.split(context)

    # Handle reference within document
    if not ref_context:
        return f"{context}{ref}"

    # Handle reference outside document
    new_ref_context = os.path.join(context_head, ref_context)
    norm_new_ref_context = os.path.normpath(new_ref_context)
    norm_case_new_ref_context = os.path.normcase(norm_new_ref_context)
    return f"{norm_case_new_ref_context}#{ref_schema}"
