"""Calculate the array schema from the artifacts."""
from open_alchemy import types

from .. import object_ref


def calculate_schema(*, artifacts: object_ref.ObjectArtifacts) -> types.Schema:
    """
    Calculate the array schema from the artifacts.

    Args:
        artifacts: The artifactsfor the array reference.

    Returns:
        The schema for the array to store with the model.

    """
    return {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": artifacts.relationship.model_name},
    }
