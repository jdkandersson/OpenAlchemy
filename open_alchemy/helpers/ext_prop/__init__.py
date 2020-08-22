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


def get(
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
    except facades.jsonschema.ValidationError as exc:
        raise exceptions.MalformedExtensionPropertyError(
            f"The value of the {json.dumps(name)} extension property is not "
            "valid. "
            f"The expected schema is {json.dumps(schema)}. "
            f"The given value is {json.dumps(value)}."
        ) from exc
    if pop:
        del source[name]  # type: ignore
    return value


def get_kwargs(
    *,
    source: typing.Union[
        typing.Dict[str, typing.Any],
        types.ColumnSchema,
        types.ObjectRefSchema,
        types.ArrayRefSchema,
        types.ReadOnlySchema,
    ],
    reserved: typing.Optional[typing.Set[str]] = None,
    default: typing.Optional[typing.Any] = None,
    pop: bool = False,
    name: str = "x-kwargs",
) -> types.TOptKwargs:
    """
    Read the value of x-kwargs, validate the schema and return it.

    Raise MalformedExtensionPropertyError when the schema of the extension property is
        malformed.
    Raise MalformedExtensionPropertyError when the keys of the kwargs are not a string.
    Raise MalformedExtensionPropertyError if any keys of x-kwargs are in the reserved
        keys.

    Args:
        source: The object to get the extension property from.
        reserved: The reserved keys that should not be in the kwargs.
        default: The default value.
        pop: Whether to remove the value from the dictionary.
        name: The name of the extension property with the kwargs.

    Returns:
        The value of the property or the default value if it does not exist.

    """
    value = get(source=source, name=name, default=default, pop=pop)
    if value is None:
        return None

    # Check for dictionary to make mypy happy, in reality always passes
    if not isinstance(value, dict):  # pragma: no cover
        raise exceptions.MalformedExtensionPropertyError(
            "The value of x-kwargs must be an object."
        )

    # Check keys are strings
    if any(not isinstance(key, str) for key in value.keys()):
        raise exceptions.MalformedExtensionPropertyError(
            "The keys of x-kwargs must be strings."
        )

    # Check whether any reserved keys are in use
    if reserved is not None:
        if not reserved.isdisjoint(value.keys()):
            raise exceptions.MalformedExtensionPropertyError(
                "Some of the keys in x-kwargs refer to arguments that OpenAlchemy "
                "handles. To make use of the arguments, please use the relevant "
                "extension property. The following keys need to be removed: "
                f"{reserved.intersection(value.keys())}."
            )

    return value
