"""Validate the schema of a model."""

# pylint: disable=unused-argument

from ... import types as oa_types
from . import types


def check(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check that a schema is valid.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The schema to validate.

    Returns:
        Whether the schema is valid with the reason if it is not.

    """
