"""Merges objects under allOf statement."""

from open_alchemy import types

from . import ref


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
        _, ref_schema = ref.resolve(name="", schema=sub_schema, schemas=schemas)
        # Merging any nested allOf
        merged_sub_schema = merge_all_of(schema=ref_schema, schemas=schemas)

        # Capturing required arrays
        merged_required = merged_schema.get("required")
        sub_required = merged_sub_schema.get("required")
        # Capturing properties
        merged_properties = merged_schema.get("properties")
        sub_properties = merged_sub_schema.get("properties")
        # Capturing backrefs
        merged_backrefs = merged_schema.get("x-backrefs")
        sub_backrefs = merged_sub_schema.get("x-backrefs")

        # Combining sub into merged specification
        merged_schema = {**merged_schema, **merged_sub_schema}

        # Checking whether required was present on both specs
        if merged_required is not None and sub_required is not None:
            # Both have a required array, need to merge them together
            required_set = set(merged_required).union(sub_required)
            merged_schema["required"] = list(required_set)

        # Checking whether properties was present on both specs
        if merged_properties is not None and sub_properties is not None:
            # Both have properties, merge properties
            merged_schema["properties"] = {**merged_properties, **sub_properties}

        # Checking whether backrefs was present on both specs
        if merged_backrefs is not None and sub_backrefs is not None:
            # Both have backrefs, merge backrefs
            merged_schema["x-backrefs"] = {**merged_backrefs, **sub_backrefs}

    return merged_schema
