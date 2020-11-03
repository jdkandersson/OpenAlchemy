"""Handle backref property."""

import typing

from open_alchemy import types
from open_alchemy.schemas.artifacts import types as artifacts_types


def handle(
    *, artifacts: artifacts_types.BackrefPropertyArtifacts
) -> typing.Tuple[typing.List, types.Schema]:
    """
    Handle readOnly object and array properties.

    Args:
        schema: The readOnly property schema.
        schemas: Used to resolve any $ref.

    Returns:
        Empty list and transformed schema.

    """
    return [], artifacts.schema
