"""Helpers for handling backrefs."""

from open_alchemy import exceptions
from open_alchemy import types


def _calculate_schema(
    *, artifacts: types.ObjectArtifacts, ref_from_array: bool, model_name: str
) -> types.Schema:
    """
    Calculate the schema for a backref.

    The key decision is whether the backref is an array. If the reference is from
    an object it is an array unless uselist is False. If the reference is from an array,
    it is not unless secondary is set to a table name.

    Args:
        artifacts: The artifacts for the object reference.
        ref_from_array: Whether the reference was from within an array.
        model_name: The name of the model defining the reference.

    Returns:
        The schema for the backref.

    """
    back_reference = artifacts.relationship.back_reference
    # Handle where back reference is None, this should not happen
    if back_reference is None:
        raise exceptions.MissingArgumentError(
            "To construct the back reference schema, back reference artifacts cannot "
            "be None"
        )

    if (
        not ref_from_array
        and (back_reference.uselist is None or back_reference.uselist is True)
    ) or (ref_from_array and artifacts.relationship.secondary is not None):
        return {"type": "array", "items": {"type": "object", "x-de-$ref": model_name}}
    return {"type": "object", "x-de-$ref": model_name}
