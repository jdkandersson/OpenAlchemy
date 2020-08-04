"""Validation for properties."""

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
    2. check that it is one of integer, number, string, boolean, object or array and
    3. check that x-json, if defined, is valid.

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

    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")

    return types.Result(True, None)
