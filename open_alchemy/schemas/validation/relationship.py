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


def _check_object_backref_uselist(
    *, schema: types.Schema, schemas: types.Schemas
) -> _OptResult:
    """Check backref and uselist for an object."""
    # Check backref
    try:
        backref = helpers.peek.backref(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return Result(False, "value of x-backref must be a string")
    # Check uselist
    try:
        uselist = helpers.peek.uselist(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return Result(False, "value of x-uselist must be a boolean")
    if uselist is False and backref is None:
        return Result(False, "a one-to-one relationship must define a back reference")

    return None


def _check_kwargs(*, schema: types.Schema, schemas: types.Schemas) -> _OptResult:
    """Check the value of x-kwargs."""
    try:
        kwargs = helpers.peek.kwargs(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return Result(False, "value of x-kwargs must be a dictionary")
    # Check for unexpected keys
    if kwargs is not None:
        unexpected_keys = {"backref", "secondary"}
        intersection = unexpected_keys.intersection(kwargs.keys())
        if intersection:
            return Result(
                False, f"x-kwargs may not contain the {next(iter(intersection))} key"
            )

    return None


def _check_object_values(*, schema: types.Schema, schemas: types.Schemas) -> _OptResult:
    """Check the values of the relationship."""
    # Check nullable
    try:
        helpers.peek.nullable(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return Result(False, "value of nullable must be a boolean")
    # Check backref and uselist
    backref_uselist_result = _check_object_backref_uselist(
        schema=schema, schemas=schemas
    )
    if backref_uselist_result is not None:
        return backref_uselist_result
    # Check foreign-key-column
    try:
        helpers.peek.foreign_key_column(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return Result(False, "value of x-foreign-key-column must be a string")
    # Check kwargs
    kwargs_result = _check_kwargs(schema=schema, schemas=schemas)
    if kwargs_result is not None:
        return kwargs_result

    return None


def _check_object(*, schema: types.Schema, schemas: types.Schemas) -> Result:
    """Check object property schema."""
    # Check $ref
    ref_result = _check_object_ref(schema=schema, schemas=schemas)
    if ref_result is not None:
        return ref_result

    # Check nullable
    values_result = _check_object_values(schema=schema, schemas=schemas)
    if values_result is not None:
        return values_result

    # Check for duplicate keys in allOf
    all_of_duplicates_result = _check_all_of_duplicates(schema=schema)
    if all_of_duplicates_result is not None:
        return all_of_duplicates_result

    return Result(True, None)


def _check_array_root(*, schema: types.Schema, schemas: types.Schemas) -> _OptResult:
    """Check for invalid keys at the array schema root."""
    # Check backref
    if helpers.peek.backref(schema=schema, schemas=schemas) is not None:
        return Result(
            False,
            "x-backref cannot be defined on x-to-many relationship property root",
        )
    # Check foreign-key-column
    if helpers.peek.foreign_key_column(schema=schema, schemas=schemas) is not None:
        return Result(
            False,
            "x-foreign-key-column cannot be defined on x-to-many relationship "
            "property root",
        )
    # Check kwargs
    if helpers.peek.kwargs(schema=schema, schemas=schemas) is not None:
        return Result(
            False, "x-kwargs cannot be defined on x-to-many relationship property root",
        )
    # Check uselist
    if helpers.peek.uselist(schema=schema, schemas=schemas) is not None:
        return Result(
            False,
            "x-uselist cannot be defined on x-to-many relationship property root",
        )

    return None


def _check_array_items_values(
    *, schema: types.Schema, schemas: types.Schemas
) -> _OptResult:
    """Check individual values of array items."""
    # Check items nullable
    items_nullable = helpers.peek.nullable(schema=schema, schemas=schemas)
    if items_nullable is True:
        return Result(False, "x-to-many relationships are not nullable")

    # Check items uselist
    items_uselist = helpers.peek.uselist(schema=schema, schemas=schemas)
    if items_uselist is False:
        return Result(False, "x-to-many relationship does not support x-uselist False")

    return None


def _check_many_to_many(*, schema: types.Schema, schemas: types.Schemas) -> _OptResult:
    """Check many to many schema."""
    # Check items secondary
    try:
        secondary = helpers.peek.secondary(schema=schema, schemas=schemas)
    except exceptions.MalformedSchemaError:
        return Result(False, "value of x-secondary must be a string")
    if secondary is None:
        return None

    # Check for foreign key column
    if helpers.peek.foreign_key_column(schema=schema, schemas=schemas) is not None:
        return Result(
            False, "many-to-many relationship does not support x-foreign-key-column"
        )

    return None


def _check_array_items(*, schema: types.Schema, schemas: types.Schemas) -> _OptResult:
    """Check the items schema."""
    # Check items type
    try:
        items_type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    except exceptions.TypeMissingError:
        return Result(False, "value of items must contain a type")
    if items_type_ != "object":
        return Result(False, "value of items must be of type object")

    # Check array item values
    _values_result = _check_array_items_values(schema=schema, schemas=schemas)
    if _values_result is not None:
        return _values_result

    # Check items as object
    object_result = _check_object(schema=schema, schemas=schemas)
    if object_result.valid is False:
        return Result(object_result.valid, f"value of items {object_result.reason}")

    # Check many to many relationship
    m2m_result = _check_many_to_many(schema=schema, schemas=schemas)
    if m2m_result is not None:
        return m2m_result

    return None


def _check_array(*, schema: types.Schema, schemas: types.Schemas) -> Result:
    """Check object property schema."""
    # Check root schema
    root_result = _check_array_root(schema=schema, schemas=schemas)
    if root_result is not None:
        return root_result

    # Retrieve items schema
    items_schema = helpers.peek.items(schema=schema, schemas=schemas)
    if items_schema is None:
        return Result(False, "array type properties must define the items schema")

    # Check items
    items_result = _check_array_items(schema=items_schema, schemas=schemas)
    if items_result is not None:
        return items_result

    return Result(True, None)


def check(schemas: types.Schemas, schema: types.Schema) -> Result:
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
