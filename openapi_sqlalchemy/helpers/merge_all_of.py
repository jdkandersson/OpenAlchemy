"""Merges objects under allOf statement."""

from openapi_sqlalchemy import types

from .resolve_ref import resolve_ref


def merge_all_of(*, schema: types.Schema, schemas: types.Schemas) -> types.Schema:
    """
    Merge schemas under allOf statement.

    Merges schemas under allOf statement which is expected to have a list of schemas.
    Any duplicate keys will be overridden. Schemas are processed in the order they are
    listed.

    Args:
        schema: The schema to operate on.
        schemas: Used to resolve any $ref.

    Returns:
        The schema with all top level allOf statements resolved.

    """
    all_of = schema.get("allOf")
    if all_of is None:
        return schema

    merged_schema: types.Schema = {}
    for sub_schema in all_of:
        # Resolving any $ref
        _, ref_schema = resolve_ref(name="", schema=sub_schema, schemas=schemas)
        # Merging any nested allOf
        merged_sub_schema = merge_all_of(schema=ref_schema, schemas=schemas)

        # Capturing required arrays
        merged_required = merged_schema.get("required")
        sub_required = merged_sub_schema.get("required")

        # Combining sub into merged specification
        merged_schema = {**merged_schema, **merged_sub_schema}

        # Checking whether required was present on both specs
        if merged_required is None or sub_required is None:
            continue

        # Both have a required array, need to merge them together with common elements
        required_set = set(merged_required).union(sub_required)
        merged_schema["required"] = list(required_set)

    return merged_schema
