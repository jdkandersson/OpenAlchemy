"""Define validation rules for relationship property schema."""

import typing

from ..... import exceptions
from ..... import helpers
from ..... import types as oa_types
from ... import types


def _check_type(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check whether the type of the property is an object or array."""
    # Check type
    try:
        type_ = helpers.peek.type_(schema=schema, schemas=schemas)
        # Check type value
        if type_ not in {"object", "array"}:
            return types.Result(False, "type not an object nor array")
        # Check for JSON
        if helpers.peek.json(schema=schema, schemas=schemas) is True:
            return types.Result(False, "property is JSON")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")
    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")

    return None


def _check_object_ref(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """
    Check whether a $ref is present and points to a constructable object.

    Assume the type of schema is object.

    """
    # Check for $ref
    ref = helpers.peek.ref(schema=schema, schemas=schemas)
    if ref is None:
        return types.Result(False, "not a reference to another object")

    # Check referenced schema is constructable
    _, ref_schema = helpers.ref.get_ref(ref=ref, schemas=schemas)
    if not helpers.schema.constructable(schema=ref_schema, schemas=schemas):
        return types.Result(False, "referenced schema not constructable")

    return None


def _check_object_backref_uselist(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check backref and uselist for an object."""
    # Check backref
    backref = helpers.peek.backref(schema=schema, schemas=schemas)
    # Check uselist
    uselist = helpers.peek.uselist(schema=schema, schemas=schemas)
    if uselist is False and backref is None:
        return types.Result(
            False, "a one-to-one relationship must define a back reference"
        )

    return None


def _check_kwargs(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check the value of x-kwargs."""
    kwargs = helpers.peek.kwargs(schema=schema, schemas=schemas)
    # Check for unexpected keys
    if kwargs is not None:
        unexpected_keys = {"backref", "secondary"}
        intersection = unexpected_keys.intersection(kwargs.keys())
        if intersection:
            return types.Result(
                False, f"x-kwargs may not contain the {next(iter(intersection))} key"
            )

    return None


def _check_object_values(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check the values of the relationship."""
    # Check nullable
    helpers.peek.nullable(schema=schema, schemas=schemas)
    # Check description
    helpers.peek.description(schema=schema, schemas=schemas)
    # Check writeOnly
    helpers.peek.write_only(schema=schema, schemas=schemas)
    # Check backref and uselist
    backref_uselist_result = _check_object_backref_uselist(
        schema=schema, schemas=schemas
    )
    if backref_uselist_result is not None:
        return backref_uselist_result
    # Check foreign-key-column
    helpers.peek.foreign_key_column(schema=schema, schemas=schemas)
    # Check kwargs
    kwargs_result = _check_kwargs(schema=schema, schemas=schemas)
    if kwargs_result is not None:
        return kwargs_result

    return None


def _check_all_of_duplicates(*, schema: oa_types.Schema) -> types.OptResult:
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
            return types.Result(
                False, f"multiple {next(iter(intersection))} defined in allOf"
            )

        # Add new keys into seen keys
        seen_keys = seen_keys.union(sub_schema_keys)

    return None


def _check_object(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.Result:
    """Check object property schema."""
    try:
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

    except exceptions.MalformedSchemaError as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")

    return types.Result(True, None)


def _check_array_root(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check for invalid keys at the array schema root."""
    # Check description
    helpers.peek.description(schema=schema, schemas=schemas)
    # Check writeOnly
    helpers.peek.write_only(schema=schema, schemas=schemas)

    # Check secondary
    if (
        helpers.peek.peek_key(schema=schema, schemas=schemas, key="x-secondary")
        is not None
    ):
        return types.Result(
            False,
            "x-secondary cannot be defined on x-to-many relationship property root",
        )
    # Check backref
    if (
        helpers.peek.peek_key(schema=schema, schemas=schemas, key="x-backref")
        is not None
    ):
        return types.Result(
            False,
            "x-backref cannot be defined on x-to-many relationship property root",
        )
    # Check foreign-key-column
    if (
        helpers.peek.peek_key(
            schema=schema, schemas=schemas, key="x-foreign-key-column"
        )
        is not None
    ):
        return types.Result(
            False,
            "x-foreign-key-column cannot be defined on x-to-many relationship "
            "property root",
        )
    # Check kwargs
    if (
        helpers.peek.peek_key(schema=schema, schemas=schemas, key="x-kwargs")
        is not None
    ):
        return types.Result(
            False,
            "x-kwargs cannot be defined on x-to-many relationship property root",
        )
    # Check uselist
    if (
        helpers.peek.peek_key(schema=schema, schemas=schemas, key="x-uselist")
        is not None
    ):
        return types.Result(
            False,
            "x-uselist cannot be defined on x-to-many relationship property root",
        )

    return None


def _check_array_items_values(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check individual values of array items."""
    # Check items nullable
    items_nullable = helpers.peek.nullable(schema=schema, schemas=schemas)
    if items_nullable is True:
        return types.Result(False, "x-to-many relationships are not nullable")

    # Check items uselist
    items_uselist = helpers.peek.uselist(schema=schema, schemas=schemas)
    if items_uselist is False:
        return types.Result(
            False, "x-to-many relationships do not support x-uselist False"
        )

    return None


def _check_many_to_many(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check many to many schema."""
    # Check items secondary
    secondary = helpers.peek.secondary(schema=schema, schemas=schemas)
    if secondary is None:
        return None

    # Check for foreign key column
    if helpers.peek.foreign_key_column(schema=schema, schemas=schemas) is not None:
        return types.Result(
            False, "many-to-many relationship does not support x-foreign-key-column"
        )

    return None


def _check_array_items(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check the items schema."""
    # Check items type
    type_result = _check_type(schema=schema, schemas=schemas)
    if type_result is not None:
        return types.Result(
            type_result.valid,
            f"items property :: {type_result.reason}".replace(" nor array", ""),
        )
    type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    if type_ != "object":
        return types.Result(
            False,
            "items property :: type not an object",
        )

    # Check array item values
    _values_result = _check_array_items_values(schema=schema, schemas=schemas)
    if _values_result is not None:
        return _values_result

    # Check items as object
    object_result = _check_object(schema=schema, schemas=schemas)
    if object_result.valid is False:
        return types.Result(
            object_result.valid, f"items property :: {object_result.reason}"
        )

    # Check many to many relationship
    m2m_result = _check_many_to_many(schema=schema, schemas=schemas)
    if m2m_result is not None:
        return m2m_result

    return None


def _check_array(*, schema: oa_types.Schema, schemas: oa_types.Schemas) -> types.Result:
    """Check object property schema."""
    try:
        # Check root schema
        root_result = _check_array_root(schema=schema, schemas=schemas)
        if root_result is not None:
            return root_result

        # Retrieve items schema
        items_schema = helpers.peek.items(schema=schema, schemas=schemas)
        if items_schema is None:
            return types.Result(
                False, "array type properties must define the items schema"
            )

        # Check items
        items_result = _check_array_items(schema=items_schema, schemas=schemas)
        if items_result is not None:
            return items_result

    except exceptions.MalformedSchemaError as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")

    return types.Result(True, None)


def check(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check whether a property schema is a valid relationship schema.

    At a high level:
    1. the type of the property must be an array or object and not JSON,
    2. the property must reference a constructable schema (at the root for x-to-one and
        at the items level for x-to-many relationships),
    3. any parameters configuring the relationship must have the expected type,
    4. in the allOf list no repeated keys are allowed,
    5. one-to-one relationship must define both x-uselist and x-backref,
    6. x-uselist and nullable is not allowed on x-to-many relationships,
    7. x-foreign-key-column is not allowed on many-to-many relationships,
    8. x-kwargs is not allowed to define backref and secondary and
    9. x-to-many relationships must define property configuration keys at the items
        level.

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
