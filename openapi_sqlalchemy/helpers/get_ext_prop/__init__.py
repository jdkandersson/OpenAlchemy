"""Read the value of an extension property, validate the schema and return it."""

import json
import os
import typing

import jsonschema

from openapi_sqlalchemy import exceptions

DIRECTORY = os.path.dirname(__file__)
SCHEMAS_FILE = os.path.join(DIRECTORY, "extension-schemas.json")
with open(SCHEMAS_FILE) as in_file:
    SCHEMAS = json.load(in_file)


def get_ext_prop(
    *, source: typing.Dict[str, typing.Any], name: str
) -> typing.Optional[typing.Union[str, bool]]:
    """
    Read the value of an extension property, validate the schema and return it.

    Raise MalformedExtensionPropertyError when the schema of the extension property is
    malformed.

    Args:
        source: The object to get the extension property from.
        name: The name of the property.

    Returns:
        The value of the property.

    """
    value = source.get(name)
    if value is None:
        return None

    schema = SCHEMAS.get(name)
    try:
        jsonschema.validate(instance=value, schema=schema)
    except jsonschema.ValidationError:
        raise exceptions.MalformedExtensionPropertyError(
            f"The value of the {json.dumps(name)} extension property is not "
            "valid. "
            f"The expected schema is {json.dumps(schema)}. "
            f"The given value is {json.dumps(value)}."
        )
    return value
