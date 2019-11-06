"""Generate columns based on OpenAPI schema property."""

import re
import typing

import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types

from . import column

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


def column_factory(
    *,
    spec: types.Schema,
    schemas: types.Schemas,
    required: typing.Optional[bool] = None,
    logical_name: str,
) -> typing.Tuple[typing.List[typing.Tuple[str, sqlalchemy.Column]], types.Schema]:
    """
    Generate column based on OpenAPI schema property.

    Args:
        spec: The schema for the column.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name and the SQLAlchemy column based on the schema.

    """
    # Checking for the type
    type_ = helpers.peek_type(schema=spec, schemas=schemas)

    # CHandling columns
    if type_ != "object":
        spec = helpers.prepare_schema(schema=spec, schemas=schemas)
        return (
            column.handle_column(
                logical_name=logical_name, spec=spec, required=required
            ),
            spec,
        )

    # Handling objects
    return _handle_object(
        spec=spec, schemas=schemas, required=required, logical_name=logical_name
    )


def _handle_object(
    *,
    spec: types.Schema,
    schemas: types.Schemas,
    required: typing.Optional[bool] = None,
    logical_name: str,
) -> typing.Tuple[
    typing.List[typing.Tuple[str, typing.Union[sqlalchemy.Column, typing.Type]]],
    types.Schema,
]:
    """
    Generate properties for a reference to another object.

    Assume that, when any $ref and allOf are resolved, the schema is an object.

    Args:
        spec: The schema for the column.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name and the SQLAlchemy column for the foreign key and the logical
        name and relationship for the reference to the object.

    """
    # Default backref
    backref = None
    # Default foreign key column
    fk_column = None

    # Checking for $ref and allOf
    ref = spec.get("$ref")
    all_of = spec.get("allOf")

    if ref is not None:
        # Handling $ref
        ref_logical_name, spec = helpers.resolve_ref(
            name=logical_name, schema=spec, schemas=schemas
        )
        backref = helpers.get_ext_prop(source=spec, name="x-backref")
    elif all_of is not None:
        # Checking for $ref, and x-backref and x-foreign-key-column counts
        _check_object_all_of(all_of_spec=all_of)

        # Handling allOf
        for sub_spec in all_of:
            backref = helpers.get_ext_prop(source=sub_spec, name="x-backref")
            fk_column = helpers.get_ext_prop(
                source=sub_spec, name="x-foreign-key-column"
            )
            if sub_spec.get("$ref") is not None:
                ref_logical_name, spec = helpers.resolve_ref(
                    name=logical_name, schema=sub_spec, schemas=schemas
                )
    else:
        raise exceptions.MalformedManyToOneRelationshipError(
            "Many to One relationships are defined using either $ref or allOf."
        )

    # Resolving allOf
    spec = helpers.merge_all_of(schema=spec, schemas=schemas)

    # If backref has not been found look in referenced schema
    if backref is None:
        backref = helpers.get_ext_prop(source=spec, name="x-backref")
    # If foreign key column has not been found look in referenced schema
    if fk_column is None:
        fk_column = helpers.get_ext_prop(source=spec, name="x-foreign-key-column")
    # If foreign key column is still None, default to id
    if fk_column is None:
        fk_column = "id"

    # Handling object
    foreign_key_spec = _handle_object_reference(
        spec=spec, schemas=schemas, fk_column=fk_column
    )
    return_value = column.handle_column(
        logical_name=f"{logical_name}_{fk_column}",
        spec=foreign_key_spec,
        required=required,
    )

    # Creating relationship
    return_value.append(
        (logical_name, sqlalchemy.orm.relationship(ref_logical_name, backref=backref))
    )
    return return_value, {"type": "object", "x-de-$ref": ref_logical_name}


def _check_object_all_of(*, all_of_spec: types.AllOfSpec) -> None:
    """
    Check format of allOf for an object reference.

    Raise MalformedManyToOneRelationshipError if the allOf schema is not as expected.

    Args:
        all_of_spec: The allOf specification to check.

    """
    # Checking for $ref and x-backref counts
    ref_count = 0
    backref_count = 0
    fk_column_count = 0
    for sub_spec in all_of_spec:
        if sub_spec.get("$ref") is not None:
            ref_count += 1
        if sub_spec.get("x-backref") is not None:
            backref_count += 1
        if sub_spec.get("x-foreign-key-column") is not None:
            fk_column_count += 1
    if ref_count != 1:
        raise exceptions.MalformedManyToOneRelationshipError(
            "Many to One relationships defined with allOf must have exactly one "
            "$ref in the allOf list."
        )
    if backref_count > 1:
        raise exceptions.MalformedManyToOneRelationshipError(
            "Many to One relationships may have at most 1 x-backref defined."
        )
    if fk_column_count > 1:
        raise exceptions.MalformedManyToOneRelationshipError(
            "Many to One relationships may have at most 1 x-foreign-key-column "
            "defined."
        )


def _handle_object_reference(
    *,
    spec: types.Schema,
    schemas: types.Schemas,
    fk_column: typing.Optional[str] = None,
) -> types.Schema:
    """
    Determine the foreign key schema for an object reference.

    Args:
        spec: The schema of the object reference.
        schemas: All defined schemas.
        fk_column: The foreign column name to use.

    Returns:
        The foreign key schema.

    """
    tablename = helpers.get_ext_prop(source=spec, name="x-tablename")
    if not tablename:
        raise exceptions.MalformedSchemaError(
            "Referenced object is missing x-tablename property."
        )
    properties = spec.get("properties")
    if properties is None:
        raise exceptions.MalformedSchemaError(
            "Referenced object does not have any properties."
        )
    fk_logical_name = fk_column if fk_column is not None else "id"
    fk_spec = properties.get(fk_logical_name)
    if fk_spec is None:
        raise exceptions.MalformedSchemaError(
            f"Referenced object does not have {fk_logical_name} property."
        )
    # Preparing specification
    prepared_fk_spec = helpers.prepare_schema(schema=fk_spec, schemas=schemas)
    fk_type = prepared_fk_spec.get("type")
    if fk_type is None:
        raise exceptions.MalformedSchemaError(
            f"Referenced object {fk_logical_name} property does not have a type."
        )

    return {"type": fk_type, "x-foreign-key": f"{tablename}.{fk_logical_name}"}
