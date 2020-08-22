"""Dictionary conversion for object."""

import typing

from ... import exceptions
from ... import helpers
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
    if value is None:
        return None

    try:
        return value.to_dict()
    except AttributeError as exc:
        raise exceptions.InvalidModelInstanceError(
            "The object property instance does not have a to_dict implementation."
        ) from exc
    except TypeError as exc:
        raise exceptions.InvalidModelInstanceError(
            "The object property instance to_dict implementation is "
            "expecting arguments."
        ) from exc


def _convert_read_only(
    *, schema: oa_types.Schema, value: typing.Any
) -> types.TOptObjectDict:
    """
    Convert readOnly value to a dictionary.

    Raise MalformedSchemaError if the schema does not have properties.
    Raise MalformedSchemaError if the schema has empty properties.
    """
    if value is None:
        return None

    properties = schema.get("properties")
    if properties is None:
        raise exceptions.MalformedSchemaError(
            "readOnly object definition must have properties."
        )
    if not isinstance(properties, dict):
        raise exceptions.MalformedSchemaError(
            "readOnly object definition must have dictionary properties."
        )
    if not properties:
        raise exceptions.MalformedSchemaError(
            "readOnly object definitions must have at least 1 property."
        )
    return_dict = {}
    for key in properties.keys():
        return_dict[key] = getattr(value, key, None)
    return return_dict


def convert(
    value: typing.Any,
    *,
    schema: oa_types.Schema,
    read_only: typing.Optional[bool] = None,
) -> types.TOptObjectDict:
    """
    Convert object schema value to dictionary.

    Args:
        value: The value to convert.
        schema: The schema for the value.
        read_only (optional): Whether the schema is read only.

    """
    schema_read_only = helpers.peek.read_only(schema=schema, schemas={})
    if read_only or schema_read_only:
        return _convert_read_only(schema=schema, value=value)
    return _convert_relationship(value=value)
