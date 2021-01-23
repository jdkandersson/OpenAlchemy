"""Convert from a dictionary to a column value."""

import typing

from ... import exceptions
from ... import types as oa_types
from ...helpers import peek
from ...helpers import type_ as type_helper
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
    type_ = peek.type_(schema=schema, schemas={})
    read_only = peek.read_only(schema=schema, schemas={})
    if read_only:
        raise exceptions.MalformedModelDictionaryError(
            "readOnly properties cannot be passed to the from_dict constructor."
        )
    json = peek.json(schema=schema, schemas={})
    if json:
        return value
    if type_ == "object":
        return object_.convert(value, schema=schema)
    if type_ == "array":
        return array.convert(value, schema=schema)
    if type_ in type_helper.SIMPLE_TYPES:
        return simple.convert(value, schema=schema)
    raise exceptions.FeatureNotImplementedError(f"Type {type_} is not supported.")
