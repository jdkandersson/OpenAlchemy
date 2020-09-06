"""Helpers to support inheritance."""

import enum
import typing

from .. import exceptions
from .. import facades
from .. import types
from . import all_of as all_of_helper
from . import ext_prop as ext_prop_helper
from . import peek as peek_helper
from . import ref as ref_helper
from . import schema as schema_helper


def check_parent(
    *, schema: types.Schema, parent_name: str, schemas: types.Schemas
) -> bool:
    """
    Check that the parent is in the inheritance chain of a schema.

    Recursive function. The base cases are:
    1. the schema has $ref where the name matches the parent name if
        a. the referenced schema is constructable, return True or
        b. if the referenced schema is not constructable, return False,
    2. the schema does not have $ref nor allOf in which case return False and
    3. The schema has $ref but the referenced schema does not inherit.

    The recursive cases are:
    1. the schema has $ref where the name does not match the parent name in which case
        the function is called with the referenced schema and
    2. the schema has allOf where the function is called on each element in allOf and,
        if True is returned for any of them, True is returned otherwise False is
        returned.

    Raise MalformedSchemaError is the value of $ref is not a string.
    Raise MalformedSchemaError if the value of allOf is not a list.
    Raise MalformedSchemaError if the parent is not found in the chain.
    Raise MalformedSchemaError if the parent does not have x-tablename nor x-inherits.
    Raise MalformedSchemaError if a $ref value is seen again.

    Args:
        schema: The schema to check.
        parent_name: The parent to check for in the inheritance chain.
        schemas: All the schemas.
        seen_refs: The $ref that have already been check to avoid circular dependencies.

    Returns:
        Whether the parent is in the inheritance chain.

    """
    return _check_parent(schema, parent_name, schemas, set())


def _check_parent(
    schema: types.Schema,
    parent_name: str,
    schemas: types.Schemas,
    seen_refs: typing.Set[str],
) -> bool:
    """Implement check_parent."""
    # Check for $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")
    if ref is None and all_of is None:
        return False

    # Handle $ref
    if ref is not None:
        if not isinstance(ref, str):
            raise exceptions.MalformedSchemaError("The value of $ref must be a string.")

        # Check for circular references
        if ref in seen_refs:
            raise exceptions.MalformedSchemaError(
                "Circular reference chain detected for the schema."
            )
        seen_refs.add(ref)

        ref_name, ref_schema = ref_helper.get_ref(ref=ref, schemas=schemas)

        # Check for name match base case
        if ref_name == parent_name:
            return schema_helper.constructable(schema=ref_schema, schemas=schemas)

        # Check referenced schema still inherits
        if schema_helper.inherits(schema=schema, schemas=schemas) is False:
            return False

        # Recursive case
        return _check_parent(ref_schema, parent_name, schemas, seen_refs)

    # Handle allOf
    if not isinstance(all_of, list):
        raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
    return any(
        _check_parent(sub_schema, parent_name, schemas, seen_refs)
        for sub_schema in all_of
    )


def get_parent(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get the name of the parent of the schema.

    Recursive function. The base cases are:
    1. the schema has $ref and the referenced schema is constructable.

    The recursive cases are:
    1. the schema has $ref where the referenced schema is not constructable in which
        case the function is called with the referenced schema and
    2. the schema has allOf in which case the return value of the first element that
        does not raise the MalformedSchemaError is returned.

    Raise MalformedSchemaError is the value of $ref is not a string.
    Raise MalformedSchemaError if the value of allOf is not a list.
    Raise MalformedSchemaError if the schema does not have $ref nor allOf.
    Raise MalformedSchemaError if the schema has allOf and all of the elements raise
        MalformedSchemaError.
    Raise MalformedSchemaError if a $ref value is seen again.

    Args:
        schema: The schema to retrieve the parent for.
        schemas: All the schemas.
        seen_refs: The $ref that have already been check to avoid circular dependencies.

    Returns:
        The name of the parent.

    """
    return _get_parent(schema, schemas, set())


def _get_parent(
    schema: types.Schema, schemas: types.Schemas, seen_refs: typing.Set[str]
) -> str:
    """Implement get_parent."""
    # Check for $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")
    if ref is None and all_of is None:
        raise exceptions.MalformedSchemaError(
            "A schema that is marked as inhereting does not reference a valid parent."
        )

    # Handle $ref
    if ref is not None:
        if not isinstance(ref, str):
            raise exceptions.MalformedSchemaError("The value of $ref must be a string.")

        # Check for circular references
        if ref in seen_refs:
            raise exceptions.MalformedSchemaError(
                "Circular reference chain detected for the schema."
            )
        seen_refs.add(ref)

        ref_name, ref_schema = ref_helper.get_ref(ref=ref, schemas=schemas)

        # Check whether the referenced schema is constructible
        if schema_helper.constructable(schema=ref_schema, schemas=schemas):
            return ref_name

        # Recursive case
        return _get_parent(ref_schema, schemas, seen_refs)

    # Handle allOf
    if not isinstance(all_of, list):
        raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
    # Find first constructable schema
    for sub_schema in all_of:
        try:
            return _get_parent(sub_schema, schemas, seen_refs)
        except exceptions.MalformedSchemaError:
            pass
    # None of the schemas in allOf are constructable
    raise exceptions.MalformedSchemaError(
        "A schema that is marked as inhereting does not reference a valid parent."
    )


def get_parents(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Generator[str, None, None]:
    """
    Retrieve all parents of a schema.

    Recursive function. Base cases:
    1. schema without $ref nor allOf then nothing is returned.

    Recursive cases:
    1. $ref in which case values are yielded from the function called with the
        referenced schema and the referenced name is yielded and
    2. allOf in which case values are yielded from the function called with each element
        of allOf.

    Raise MalformedSchemaError is the value of $ref is not a string.
    Raise MalformedSchemaError if the value of allOf is not a list.
    Raise MalformedSchemaError if the same $ref value is seen again.

    Args:
        schema: The schema to retrieve all parents for.
        schemas: All the schemas.

    Returns:
        A generator with all parents of the schema.

    """
    return _get_parents(schema, schemas, set())


def _get_parents(
    schema: types.Schema, schemas: types.Schemas, seen_refs: typing.Set[str]
) -> typing.Generator[str, None, None]:
    """Implement get_parents."""
    # Check for $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")

    # Handle $ref
    if ref is not None:
        if not isinstance(ref, str):
            raise exceptions.MalformedSchemaError("The value of $ref must be a string.")

        # Check for circular references
        if ref in seen_refs:
            raise exceptions.MalformedSchemaError(
                "Circular reference chain detected for the schema."
            )
        seen_refs.add(ref)

        ref_name, ref_schema = ref_helper.get_ref(ref=ref, schemas=schemas)

        # Check for inherits
        if schema_helper.inherits(schema=schema, schemas=schemas):
            yield from _get_parents(ref_schema, schemas, seen_refs)

        if schema_helper.constructable(schema=ref_schema, schemas=schemas):
            yield ref_name
        return

    # Handle allOf
    if all_of is not None:
        if not isinstance(all_of, list):
            raise exceptions.MalformedSchemaError("The value of allOf must be a list.")
        for sub_schema in all_of:
            yield from _get_parents(sub_schema, schemas, seen_refs)


def retrieve_parent(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get or check the name of the parent.

    If x-inherits is True, get the name of the parent. If it is a string, check the
    parent.

    Raise InheritanceError if x-inherits is not defined or False.

    Args:
        schema: The schema to retrieve the parent for.
        schemas: All the schemas.

    Returns:
        The parent.

    """
    inherits = peek_helper.inherits(schema=schema, schemas=schemas)
    if inherits is True:
        return get_parent(schema=schema, schemas=schemas)
    if isinstance(inherits, str):
        if not check_parent(schema=schema, parent_name=inherits, schemas=schemas):
            raise exceptions.InheritanceError(
                f"The x-inherits value {inherits} is not a valid parent."
            )
        return inherits
    raise exceptions.InheritanceError(
        "Cannot retrieve the name of the parent if x-inherits is not defined or False."
    )


def retrieve_model_parents_schema(schema: types.Schema) -> types.Schema:
    """
    Retrieve the combined schema of the input and all its parent schemas.

    Args:
        schema: The model schema. Assume that it does not contain any $ref nor allOf.

    Returns:
        The combined schema.

    """
    schemas = _retrieve_model_parents_schema(schema)
    schema = {"allOf": schemas}
    return all_of_helper.merge(schema=schema, schemas={})


def _retrieve_model_parents_schema(
    schema: types.Schema,
) -> typing.Generator[types.Schema, None, None]:
    """
    Retrieve all the schemas of the inheritance chain, including the initial schema.

    Recursive function. Base case is schema without x-inherits where schema is yielded.
    Recursive case is schema with x-inherits where the function is called on the parent
    schema and then the schema is yielded.

    Args:
        schema: The model schema. Assume that it does not contain any $ref nor allOf.

    Returns:
        Generator with all the schemas.

    """
    inherits = ext_prop_helper.get(source=schema, name="x-inherits")
    if isinstance(inherits, str):
        parent_schema = facades.models.get_model_schema(name=inherits)
        if parent_schema is None:
            raise exceptions.InheritanceError(f"The parent {inherits} is not defined.")
        yield from _retrieve_model_parents_schema(parent_schema)
    yield schema


@enum.unique
class Type(str, enum.Enum):
    """The type of inheritance."""

    NONE = "NONE"
    JOINED_TABLE = "JOINED_TABLE"
    SINGLE_TABLE = "SINGLE_TABLE"


def calculate_type(*, schema: types.Schema, schemas: types.Schemas) -> Type:
    """
    Calculate the type of inheritance.

    Assume the schema and any parent schema is constructable and valid.

    The rules are:
    1. if the schema does not inherit return NONE,
    2. if the parent and child tablename are different return JOINED_TABLE and
    3. else return SINGLE_TABLE.

    Args:
        schema: The schema to calculate the type for.
        schemas: All defined schemas used to resolve any $ref.

    Returns:
        The type of inheritance.

    """
    if not schema_helper.inherits(schema=schema, schemas=schemas):
        return Type.NONE

    parent = retrieve_parent(schema=schema, schemas=schemas)
    parent_schema = schemas[parent]
    parent_tablename = peek_helper.tablename(schema=parent_schema, schemas=schemas)
    tablename = peek_helper.prefer_local(
        get_value=peek_helper.tablename, schema=schema, schemas=schemas
    )

    if parent_tablename == tablename:
        return Type.SINGLE_TABLE
    return Type.JOINED_TABLE
