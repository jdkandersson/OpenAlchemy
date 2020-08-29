"""Helpers that clean up."""

from ... import types


def extension(*, schema: types.Schema) -> None:
    """
    Remove extension properties from a schema.

    Args:
        schema: The schema to clean.

    """
    extension_keys = list(filter(lambda key: key.startswith("x-"), schema.keys()))
    for key in extension_keys:
        del schema[key]
