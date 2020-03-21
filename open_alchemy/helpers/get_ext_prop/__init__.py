"""Read the value of an extension property, validate the schema and return it."""

import json
import os
import typing

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import types

_DIRECTORY = os.path.dirname(__file__)
_SCHEMAS_FILE = os.path.join(_DIRECTORY, "extension-schemas.json")
_COMMON_SCHEMAS_FILE = os.path.join(_DIRECTORY, "common-schemas.json")
_resolver, (_SCHEMAS, _) = facades.jsonschema.resolver(  # pylint: disable=invalid-name
    _SCHEMAS_FILE, _COMMON_SCHEMAS_FILE
)


def get_ext_prop(
    *,
    source: typing.Union[
        typing.Dict[str, typing.Any],
        types.ColumnSchema,
        types.ObjectRefSchema,
        types.ArrayRefSchema,
        types.ReadOnlySchema,
    ],
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
    # Check for presence of name
    if name not in source:
        return default

    # Retrieve value
    value = source.get(name)
    if value is None:
        raise exceptions.MalformedExtensionPropertyError(
            f"The value of the {name} extension property cannot be null."
        )

    schema = _SCHEMAS.get(name)
    try:
        facades.jsonschema.validate(instance=value, schema=schema, resolver=_resolver)
    except facades.jsonschema.ValidationError:
        raise exceptions.MalformedExtensionPropertyError(
            f"The value of the {json.dumps(name)} extension property is not "
            "valid. "
            f"The expected schema is {json.dumps(schema)}. "
            f"The given value is {json.dumps(value)}."
        )
    if pop:
        del source[name]  # type: ignore
    return value
