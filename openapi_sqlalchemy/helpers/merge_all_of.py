"""Merges objects under allOf statement."""

from openapi_sqlalchemy import types


def merge_all_of(*, spec: types.SchemaSpec) -> types.SchemaSpec:
    """
    Merge specifications under allOf statement.

    Merges objects under allOf statement which is expected to have a list of objects.
    Any duplicate keys will be overridden. Objects are processed in the order they are
    listed.

    Args:
        spec: The specification to operate on.

    Returns:
        The specification with all top level allOf statements resolved.

    """
    all_of = spec.get("allOf")
    if all_of is None:
        return spec

    merged_spec: types.SchemaSpec = {}
    for sub_spec in all_of:
        merged_spec = {**merged_spec, **sub_spec}
    return merged_spec
