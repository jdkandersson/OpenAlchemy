"""Define validation rules for simple properties."""

from .... import exceptions
from .... import helpers
from .... import types as oa_types
from .. import types

TYPES = {"integer", "number", "string", "boolean"}

# Set of valid type and format combinations
_VALID_TYPE_FORMAT = {
    ("integer", None),
    ("integer", "int32"),
    ("integer", "int64"),
    ("number", None),
    ("number", "float"),
    ("string", None),
    ("string", "password"),
    ("string", "byte"),
    ("string", "binary"),
    ("string", "date"),
    ("string", "date-time"),
    ("boolean", None),
}
_VALID_MAX_LENGTH_TYPE_FORMAT = {
    ("string", None),
    ("string", "password"),
    ("string", "byte"),
    ("string", "binary"),
}


def _check_modifiers(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check property schema modifiers."""
    # check type
    type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    if type_ not in TYPES:
        return types.Result(False, f"{type_} type is not supported")

    # check format
    format_ = helpers.peek.format_(schema=schema, schemas=schemas)
    type_format = (type_, format_)
    # Check type and format combination
    if type_format not in _VALID_TYPE_FORMAT:
        return types.Result(False, f"{format_} format is not supported for {type_}")

    # Define format display value
    format_str = ""
    if format_ is not None:
        format_str = f" {format_} format"

    # Check maxLength
    max_length = helpers.peek.max_length(schema=schema, schemas=schemas)
    if max_length is not None and type_format not in _VALID_MAX_LENGTH_TYPE_FORMAT:
        return types.Result(False, f"{type_}{format_str} does not support maxLength")

    # Check autoincrement
    autoincrement = helpers.peek.autoincrement(schema=schema, schemas=schemas)
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
    kwargs = helpers.peek.kwargs(schema=schema, schemas=schemas)
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
    foreign_key = helpers.peek.foreign_key(schema=schema, schemas=schemas)

    # Check foreign key kwargs
    foreign_key_kwargs = helpers.peek.foreign_key_kwargs(schema=schema, schemas=schemas)
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
        helpers.peek.nullable(schema=schema, schemas=schemas)
        # Check primary_key
        helpers.peek.primary_key(schema=schema, schemas=schemas)
        # Check index
        helpers.peek.index(schema=schema, schemas=schemas)
        # Check unique
        helpers.peek.unique(schema=schema, schemas=schemas)
        # Check description
        helpers.peek.description(schema=schema, schemas=schemas)
        # Check default
        helpers.peek.default(schema=schema, schemas=schemas)
        # Check writeOnly
        helpers.peek.write_only(schema=schema, schemas=schemas)

    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")
    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")

    return types.Result(True, None)
