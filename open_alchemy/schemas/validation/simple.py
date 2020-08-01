"""Define validation rules for simple properties."""

# pylint: disable=unused-argument,unused-variable

from ... import exceptions
from ... import helpers
from ... import types as oa_types
from . import types


def check(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check the schema of a simple property (not an object nor an array).

    Args:
        schemas: The schemas used to resolve any $ref.
        schema: The schema of the property.

    Returns:
        A result with whether the schema is valid and a reason if it is not.

    """
    # check type
    try:
        type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    except exceptions.SchemaNotFoundError:
        return types.Result(False, "reference does not resolve")
    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema when retrieving the type: {exc}")
    if type_ not in {"integer", "number", "string", "boolean"}:
        return types.Result(False, f"{type_} type is not supported")

    return types.Result(True, None)
