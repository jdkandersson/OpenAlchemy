"""Read the value of an extension property, validate the schema and return it."""

import json
import os
import typing

import jsonschema

from open_alchemy import exceptions

_DIRECTORY = os.path.dirname(__file__)
_SCHEMAS_FILE = os.path.join(_DIRECTORY, "extension-schemas.json")
with open(_SCHEMAS_FILE) as in_file:
    _SCHEMAS = json.load(in_file)
_COMMON_SCHEMAS_FILE = os.path.join(_DIRECTORY, "common-schemas.json")
with open(_COMMON_SCHEMAS_FILE) as in_file:
    _COMMON_SCHEMAS = json.load(in_file)
_resolver = jsonschema.RefResolver.from_schema(  # pylint: disable=invalid-name
    {**_COMMON_SCHEMAS, **_SCHEMAS}
)


def get_ext_prop(
    *,
    source: typing.Dict[str, typing.Any],
    name: str,
    default: typing.Optional[typing.Any] = None,
    pop: bool = False,
) -> typing.Optional[typing.Any]:
    """
    Read the value of an extension property, validate the schema and return it.

    Raise MalformedExtensionPropertyError when the schema of the extension property is
    malformed.

    Args:
        source: The object to get the extension property from.
        name: The name of the property.
        default: The default value.
        pop: Whether to remove the value from the dictionary.

    Returns:
        The value of the property or the default value if it does not exist.

    """
    value = source.get(name)
    if value is None:
        return default

    schema = _SCHEMAS.get(name)
    try:
        jsonschema.validate(instance=value, schema=schema, resolver=_resolver)
    except jsonschema.ValidationError:
        raise exceptions.MalformedExtensionPropertyError(
            f"The value of the {json.dumps(name)} extension property is not "
            "valid. "
            f"The expected schema is {json.dumps(schema)}. "
            f"The given value is {json.dumps(value)}."
        )
    if pop:
        del source[name]
    return value
