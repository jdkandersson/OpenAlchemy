"""Merges objects under allOf statement."""

from openapi_sqlalchemy import types


def merge_all_of(*, schema: types.SchemaSpec) -> types.SchemaSpec:
    """
    Merge schemas under allOf statement.

    Args:
        schema: The schema to operate on.

    Returns:
        The schema with all top level allOf statements resolved.

    """
    all_of = schema.get("allOf")
    if all_of is None:
        return schema

    merged_schema: types.SchemaSpec = {}
    for sub_schema in all_of:
        merged_schema = {**merged_schema, **sub_schema}
    return merged_schema
