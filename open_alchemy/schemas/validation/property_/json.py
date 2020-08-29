"""Define validation rules for JSON properties."""

from .... import exceptions
from .... import helpers
from .... import types as oa_types
from .. import types
from . import simple


def check(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check the schema of a simple property (not an object nor an array).

    Args:
        schemas: The schemas used to resolve any $ref.
        schema: The schema of the property.

    Returns:
        A result with whether the schema is valid and a reason if it is not.

    """
    try:
        helpers.peek.nullable(schema=schema, schemas=schemas)
        helpers.peek.description(schema=schema, schemas=schemas)
        helpers.peek.read_only(schema=schema, schemas=schemas)
        helpers.peek.write_only(schema=schema, schemas=schemas)
        helpers.peek.index(schema=schema, schemas=schemas)
        helpers.peek.unique(schema=schema, schemas=schemas)
        helpers.peek.primary_key(schema=schema, schemas=schemas)
        autoincrement = helpers.peek.peek_key(
            schema=schema, schemas=schemas, key="x-autoincrement"
        )
        if autoincrement is not None:
            return types.Result(False, "json properties do not support x-autoincrement")
        helpers.peek.foreign_key(schema=schema, schemas=schemas)
        kwargs_result = simple.check_kwargs(schema=schema, schemas=schemas)
        if kwargs_result is not None:
            return kwargs_result

    except exceptions.MalformedSchemaError as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")

    return types.Result(True, None)
