"""Calculate the array schema from the artifacts."""

from open_alchemy import types


def calculate_schema(*, artifacts: types.ObjectArtifacts) -> types.Schema:
    """
    Calculate the array schema from the artifacts.

    Args:
        artifacts: The artifactsfor the array reference.

    Returns:
        The schema for the array to store with the model.

    """
    return {"type": "object", "x-de-$ref": artifacts.relationship.model_name}
