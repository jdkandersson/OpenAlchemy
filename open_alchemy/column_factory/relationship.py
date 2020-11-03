"""Construct column for relationship property."""

import typing

from open_alchemy import facades
from open_alchemy import types as oa_types
from open_alchemy.schemas.artifacts import types as artifact_types

from . import types


def handle(
    *, logical_name: str, artifacts: artifact_types.TAnyRelationshipPropertyArtifacts
) -> typing.Tuple[
    types.TReturnValue, typing.Union[oa_types.ObjectRefSchema, oa_types.ArrayRefSchema]
]:
    """
    Handle a json column.

    Args:
        artifacts: The artifacts of the json column.

    Returns:
        The constructed column.

    """
    return (
        [
            (
                logical_name,
                facades.sqlalchemy.relationship.construct(artifacts=artifacts),
            )
        ],
        artifacts.schema,
    )
