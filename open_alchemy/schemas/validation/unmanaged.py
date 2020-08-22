"""Check unmanaged schemas for why they are unmanaged."""

from ... import exceptions
from ... import helpers as _oa_helpers
from ... import types as _oa_types
from . import types


def _reason_to_result(*, reason: str) -> types.TResult:
    """Convert a reason to a result."""
    return {"valid": False, "reason": reason}


def check_model(schemas: _oa_types.Schemas, schema: _oa_types.Schema) -> types.TModel:
    """
    Check a model.

    Algorithm:
    1. check for type
    2. check that type is object and
    3. check for tablename.

    Args:
        schema: The schema of the model to check.

    Returns:
        Whether the model and its properties are valid with a reason if it is not.

    """
    try:
        # Check type
        type_ = _oa_helpers.peek.peek_key(schema=schema, schemas=schemas, key="type")
        if type_ is None:
            return {
                "result": _reason_to_result(
                    reason='no "type" key was found, define a type'
                )
            }
        if not isinstance(type_, str):
            return {
                "result": _reason_to_result(
                    reason="the type value is True, change it to a string value"
                )
            }
        if type_ != "object":
            return {
                "result": _reason_to_result(
                    reason=(
                        f'the type of the schema is "{type_}", change it to be "object"'
                    )
                )
            }

    except exceptions.MalformedSchemaError as exc:
        return {"result": _reason_to_result(reason=f"malformed schema :: {exc}")}
    except exceptions.SchemaNotFoundError as exc:
        return {"result": _reason_to_result(reason=f"reference :: {exc}")}

    # tablename is not defined
    return {
        "result": _reason_to_result(
            reason='no "x-tablename" key was found, define the name of the table'
        )
    }
