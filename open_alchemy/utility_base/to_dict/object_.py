"""Dictionary conversion for object."""

import typing

from ... import exceptions
from ... import types as oa_types
from .. import types


def _convert_relationship(*, value: types.TModel) -> types.TOptObjectDict:
    """
    Convert object relationship property to a dictionary.

    Raises InvalidModelInstanceError if the value does not have a to_dict function.
    Raises InvalidModelInstanceError if the value has a to_dict function that expects
        arguments.

    Args:
        value: The value to convert.

    Returns:
        The object as a dictionary.

    """
    try:
        return value.to_dict()
    except AttributeError:
        raise exceptions.InvalidModelInstanceError(
            f"The object property instance does not have a to_dict " "implementation."
        )
    except TypeError:
        raise exceptions.InvalidModelInstanceError(
            f"The object property instance to_dict implementation is "
            "expecting arguments."
        )


def _convert_read_only(
    *, schema: oa_types.Schema, value: typing.Any
) -> types.TOptObjectDict:
    """
    Convert readOnly value to a dictionary.

    Raise MalformedSchemaError if the schema does not have properties.
    Raise MalformedSchemaError if the schema has empty properties.
    """
    properties = schema.get("properties")
    if properties is None:
        raise exceptions.MalformedSchemaError(
            f"readOnly object definition must have properties."
        )
    if not isinstance(properties, dict):
        raise exceptions.MalformedSchemaError(
            f"readOnly object definition must have dictionary properties."
        )
    if not properties:
        raise exceptions.MalformedSchemaError(
            f"readOnly object definitions must have at least 1 property."
        )
    return_dict = {}
    for key in properties.keys():
        return_dict[key] = getattr(value, key, None)
    return return_dict
