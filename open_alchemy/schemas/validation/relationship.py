"""Define validation rules for relationship."""

import typing

from ... import exceptions
from ... import helpers
from ... import types


class Result(typing.NamedTuple):
    """Result of checking a schema."""

    # Whether the schema is valid
    valid: bool
    # If not valid, the reason why it isn't
    reason: typing.Optional[str]


_OptResult = typing.Optional[Result]


def _check_type(*, schema: types.Schema, schemas: types.Schemas) -> _OptResult:
    """Check whether the type of the property is an object or array."""
    # Check type
    try:
        type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    except exceptions.TypeMissingError:
        return Result(False, "type missing")
    except exceptions.SchemaNotFoundError:
        return Result(False, "reference does not resolve")
    if type_ not in {"object", "array"}:
        return Result(False, "type not an object nor array")

    return None


def _check_all_of_duplicates(*, schema: types.Schema) -> _OptResult:
    """Check for duplicate keys in allOf."""
    # Retrieve allOf
    all_of = schema.get("allOf")
    if all_of is None:
        return None

    # Check for duplicate keys
    seen_keys: typing.Set[str] = set()
    for sub_schema in all_of:
        # Check whether any keys have already been seen
        sub_schema_keys = sub_schema.keys()
        intersection = seen_keys.intersection(sub_schema_keys)
        if intersection:
            return Result(
                False, f"multiple {next(iter(intersection))} defined in allOf"
            )

        # Add new keys into seen keys
        seen_keys = seen_keys.union(sub_schema_keys)

    return None


def _check_object_ref(*, schema: types.Schema, schemas: types.Schemas) -> _OptResult:
    """
    Check whether a $ref is present and points to a constructable object.

    Assume the type of schema is object.

    """
    # Check for $ref
    ref = helpers.peek.ref(schema=schema, schemas=schemas)
    if ref is None:
        return Result(False, "not a reference to another object")

    # Check referenced schema is constructable
    _, ref_schema = helpers.ref.resolve(schema={"$ref": ref}, schemas=schemas, name="")
    if not helpers.schema.constructable(schema=ref_schema, schemas=schemas):
        return Result(False, "referenced schema not constructable")

    return None


def _check_object(*, schema: types.Schema, schemas: types.Schemas) -> Result:
    """Check object property schema."""
    # Check $ref
    ref_result = _check_object_ref(schema=schema, schemas=schemas)
    if ref_result is not None:
        return ref_result

    # Check nullable
    try:
        helpers.peek.nullable(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return Result(False, "value of nullable must be a boolean")

    # Check for duplicate keys in allOf
    all_of_duplicates_result = _check_all_of_duplicates(schema=schema)
    if all_of_duplicates_result is not None:
        return all_of_duplicates_result

    return Result(True, None)


def _check_array(*, schema: types.Schema, schemas: types.Schemas) -> _OptResult:
    """Check object property schema."""
    # Retrieve items schema
    items_schema = helpers.peek.items(schema=schema, schemas=schemas)
    if items_schema is None:
        return Result(False, "array type properties must define the items schema")

    # Check items type
    try:
        items_type_ = helpers.peek.type_(schema=items_schema, schemas=schemas)
    except exceptions.TypeMissingError:
        return Result(False, "value of items must contain a type")
    if items_type_ != "object":
        return Result(False, "value of items must be of type object")

    # Check $ref
    items_ref_result = _check_object_ref(schema=items_schema, schemas=schemas)
    if items_ref_result is not None:
        return Result(
            items_ref_result.valid, f"value of items {items_ref_result.reason}"
        )

    return None


def check(schemas: types.Schemas, schema: types.Schema) -> _OptResult:
    """
    Check whether a property schema is a valid relationship schema.

    Args:
        schemas: All the defined schemas used to resolve any $ref.
        schema: The schema to check.

    Returns:
        Whether the schema is a valid relationship.

    """
    # Check type
    type_result = _check_type(schema=schema, schemas=schemas)
    if type_result is not None:
        return type_result

    # Handle object
    type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    if type_ == "object":
        return _check_object(schema=schema, schemas=schemas)

    # Handle array
    return _check_array(schema=schema, schemas=schemas)
