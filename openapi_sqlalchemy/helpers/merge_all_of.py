"""Merges objects under allOf statement."""

from openapi_sqlalchemy import types

from .resolve_ref import resolve_ref


def merge_all_of(*, spec: types.SchemaSpec, schemas: types.Schemas) -> types.SchemaSpec:
    """
    Merge specifications under allOf statement.

    Merges objects under allOf statement which is expected to have a list of objects.
    Any duplicate keys will be overridden. Objects are processed in the order they are
    listed.

    Args:
        spec: The specification to operate on.
        schemas: Used to resolve any $ref.

    Returns:
        The specification with all top level allOf statements resolved.

    """
    all_of = spec.get("allOf")
    if all_of is None:
        return spec

    merged_spec: types.SchemaSpec = {}
    for sub_spec in all_of:
        # Resolving any $ref
        resolved_spec = resolve_ref(
            schema=types.Schema(logical_name="", spec=sub_spec), schemas=schemas
        ).spec
        # Merging any nested allOf
        merged_sub_spec = merge_all_of(spec=resolved_spec, schemas=schemas)
        # Combining sub into merged specification
        merged_spec = {**merged_spec, **merged_sub_spec}
    return merged_spec
