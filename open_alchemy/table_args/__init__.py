"""Construct table args for a model."""

import json
import os
import typing

import jsonschema

from open_alchemy import exceptions
from open_alchemy import types

_DIRECTORY = os.path.dirname(__file__)
_PATHS = ("..", "helpers", "get_ext_prop", "common-schemas.json")
_COMMON_SCHEMAS_FILE = os.path.join(_DIRECTORY, *_PATHS)
with open(_COMMON_SCHEMAS_FILE) as in_file:
    _COMMON_SCHEMAS = json.load(in_file)
_resolver = jsonschema.RefResolver.from_schema(  # pylint: disable=invalid-name
    _COMMON_SCHEMAS
)


def _spec_to_schema_name(
    *, spec: types.Schema, schema_names: typing.Optional[typing.List[str]] = None
) -> str:
    """
    Convert a specification to the name of the matched schema.

    Use the schema names defined in common-schemas.json to find the first matching
    schema.

    Args:
        spec: The specification to convert.
        schema_names: The names of the schemas to check.

    Returns:
        The name of the specification.

    """
    if schema_names is None:
        schema_names = _COMMON_SCHEMAS.keys()

    for name in schema_names:
        try:
            jsonschema.validate(
                instance=spec, schema=_COMMON_SCHEMAS[name], resolver=_resolver
            )
            return name
        except jsonschema.ValidationError:
            continue
    raise exceptions.SchemaNotFoundError("Specification did not match any schemas.")
