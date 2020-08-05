"""Validation for properties."""

import enum

from .... import exceptions
from .... import helpers
from .... import types as oa_types
from .. import types
from . import relationship
from . import simple

_SUPPORTED_TYPES = {"integer", "number", "string", "boolean", "object", "array"}


def check_type(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check whether the type of a property can be calculated.

    Algorithm:
    1. check that the type is present and valid
    2. check that it is one of integer, number, string, boolean, object or array,
    3. check that x-json, if defined, is valid and
    3. check that readOnly, if defined, is valid.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The property schema to check.

    Returns:
        Whether thetype of the property can be determined.

    """
    try:
        type_ = helpers.peek.type_(schema=schema, schemas=schemas)
        if type_ not in _SUPPORTED_TYPES:
            return types.Result(False, f"{type_} is not a supported type")
        helpers.peek.json(schema=schema, schemas=schemas)
        helpers.peek.read_only(schema=schema, schemas=schemas)

    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")

    return types.Result(True, None)


class Type(enum.Enum):
    """The type of a property."""

    READ_ONLY = 1
    SIMPLE = 2
    JSON = 3
    RELATIONSHIP = 4


def calculate_type(schemas: oa_types.Schemas, schema: oa_types.Schema) -> Type:
    """
    Calculate the type of the property.

    Assume the property has a valid type.

    The rules are:
    1. if x-json is True it is JSON,
    2. if readOnly is True it is READ_ONLY,
    2. if it is type object or array it is RELATIONSHIP and
    3. otherwise it is SIMPLE.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The schema to calculate the type for.

    Returns:
        The type of the property.

    """
    json = helpers.peek.json(schema=schema, schemas=schemas)
    if json is True:
        return Type.JSON

    read_only = helpers.peek.read_only(schema=schema, schemas=schemas)
    if read_only is True:
        return Type.READ_ONLY

    type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    if type_ in {"object", "array"}:
        return Type.RELATIONSHIP
    return Type.SIMPLE
