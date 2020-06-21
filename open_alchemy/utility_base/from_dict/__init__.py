"""Convert from a dictionary to a column value."""

import typing

from ... import exceptions
from ... import helpers
from ... import types as oa_types
from .. import types
from . import array
from . import object_
from . import simple


def convert(*, schema: oa_types.Schema, value: typing.Any) -> types.TAnyCol:
    """
    Convert value for a schema to a dictionary.

    Args:
        value: The value to convert.
        schema: The schema of the value.

    Returns:
        The converted value.

    """
    type_ = helpers.peek.type_(schema=schema, schemas={})
    read_only = helpers.peek.read_only(schema=schema, schemas={})
    if read_only:
        raise exceptions.MalformedModelDictionaryError(
            "readOnly properties cannot be passed to the from_dict constructor."
        )
    json = helpers.peek.json(schema=schema, schemas={})
    if json:
        return value
    if type_ == "object":
        return object_.convert(value, schema=schema)
    if type_ == "array":
        return array.convert(value, schema=schema)
    if type_ in {"integer", "number", "string", "boolean"}:
        return simple.convert(value, schema=schema)
    raise exceptions.FeatureNotImplementedError(f"Type {type_} is not supported.")
