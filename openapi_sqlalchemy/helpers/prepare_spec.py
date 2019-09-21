"""Aggregates helpers required to use a spec."""

from openapi_sqlalchemy import types

from .merge_all_of import merge_all_of
from .resolve_ref import resolve_ref


def prepare_spec(*, spec: types.SchemaSpec, schemas: types.Schemas) -> types.SchemaSpec:
    """
    Prepare a specification for use.

    Resolves $ref and merges allOf statements before returning the specification.

    Args:
        spec: The spec to prepare.
        schemas: All the specifications that could be use in a $ref.

    Returns:
        The specification that is ready for use.

    """
    # Resolving any root $ref
    resolved_spec = resolve_ref(
        schema=types.Schema(logical_name="", spec=spec), schemas=schemas
    ).spec
    merged_spec = merge_all_of(spec=resolved_spec, schemas=schemas)
    return merged_spec
