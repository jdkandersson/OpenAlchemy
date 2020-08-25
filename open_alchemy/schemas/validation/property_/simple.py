"""Define validation rules for simple properties."""

from .... import exceptions
from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types

TYPES = helpers.property_.simple.TYPES

# Set of valid type and format combinations
_VALID_TYPE_FORMAT = {
    ("integer", None),
    ("integer", "int32"),
    ("integer", "int64"),
    ("number", None),
    ("number", "float"),
    ("boolean", None),
}


def _check_modifiers(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check property schema modifiers."""
    # check type
    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    if type_ not in TYPES:
        return types.Result(False, f"{type_} type is not supported")

    # check format
    format_ = oa_helpers.peek.format_(schema=schema, schemas=schemas)
    type_format = (type_, format_)
    # Check type and format combination
    if type_ != "string" and type_format not in _VALID_TYPE_FORMAT:
        return types.Result(False, f"{format_} format is not supported for {type_}")

    # Define format display value
    format_str = ""
    if format_ is not None:
        format_str = f" {format_} format"

    # Check maxLength
    max_length = oa_helpers.peek.max_length(schema=schema, schemas=schemas)
    if max_length is not None:
        if type_ != "string" or format_ in {"date", "date-time"}:
            return types.Result(
                False, f"{type_}{format_str} does not support maxLength"
            )

    # Check autoincrement
    autoincrement = oa_helpers.peek.autoincrement(schema=schema, schemas=schemas)
    if autoincrement is not None and type_ != "integer":
        return types.Result(
            False, f"{type_}{format_str} does not support x-autoincrement"
        )

    return None


def check_kwargs(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check the value of kwargs."""
    # Check kwargs
    kwargs = oa_helpers.peek.kwargs(schema=schema, schemas=schemas)
    # Check for unexpected keys
    if kwargs is not None:
        unexpected_keys = {
            "nullable",
            "default",
            "primary_key",
            "autoincrement",
            "index",
            "unique",
        }
        intersection = unexpected_keys.intersection(kwargs.keys())
        if intersection:
            return types.Result(
                False, f"x-kwargs :: may not contain the {next(iter(intersection))} key"
            )

    # Check foreign_key
    foreign_key = oa_helpers.peek.foreign_key(schema=schema, schemas=schemas)

    # Check foreign key kwargs
    foreign_key_kwargs = oa_helpers.peek.foreign_key_kwargs(
        schema=schema, schemas=schemas
    )
    if foreign_key_kwargs is not None and foreign_key is None:
        return types.Result(
            False, "x-foreign-key-kwargs :: can only be defined alongside x-foreign-key"
        )

    return None


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
        # Check modifiers
        modifiers_result = _check_modifiers(schema=schema, schemas=schemas)
        if modifiers_result is not None:
            return modifiers_result

        # Check kwargs
        kwargs_result = check_kwargs(schema=schema, schemas=schemas)
        if kwargs_result is not None:
            return kwargs_result

        # Check nullable
        oa_helpers.peek.nullable(schema=schema, schemas=schemas)
        # Check primary_key
        oa_helpers.peek.primary_key(schema=schema, schemas=schemas)
        # Check index
        oa_helpers.peek.index(schema=schema, schemas=schemas)
        # Check unique
        oa_helpers.peek.unique(schema=schema, schemas=schemas)
        # Check description
        oa_helpers.peek.description(schema=schema, schemas=schemas)
        # Check default
        oa_helpers.peek.default(schema=schema, schemas=schemas)
        # Check writeOnly
        oa_helpers.peek.write_only(schema=schema, schemas=schemas)

    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")
    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")

    return types.Result(True, None)
