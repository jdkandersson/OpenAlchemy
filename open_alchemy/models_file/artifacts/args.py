"""Artifacts for the arguments."""

import json
import typing

from open_alchemy import helpers
from open_alchemy import schemas
from open_alchemy import types as oa_types

from .. import types


class ReturnValue(typing.NamedTuple):
    """The return value for the calculated artifacts."""

    required: typing.List[types.ColumnArtifacts]
    not_required: typing.List[types.ColumnArtifacts]


def _map_default(
    *, artifacts: schemas.artifacts.types.TAnyPropertyArtifacts
) -> oa_types.TColumnDefault:
    """
    Map default value from OpenAPI to be ready to be inserted into a Python file.

    First applies JSON formatting for a string and then using the type mapping helper
    function.

    Args:
        artifacts: The artifacts from which to map the default value.

    Returns:
        The mapped default value.

    """
    if artifacts.type != schemas.helpers.property_.type_.Type.SIMPLE:
        return None

    default = artifacts.open_api.default
    if default is None:
        return None

    # Escape string
    if artifacts.open_api.type == "string" and artifacts.open_api.format not in {
        "date",
        "date-time",
    }:
        default = json.dumps(default)

    # Handle bytes
    if artifacts.open_api.type == "string" and artifacts.open_api.format == "binary":
        return f"b{default}"

    # Map type
    mapped_default = helpers.oa_to_py_type.convert(
        value=default, type_=artifacts.open_api.type, format_=artifacts.open_api.format
    )

    # Get the repr if it isn't a float, bool, number nor str
    if isinstance(mapped_default, (int, float, str, bool)):
        return mapped_default
    return repr(mapped_default)
