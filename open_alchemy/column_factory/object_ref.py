"""Functions relating to object references."""

import dataclasses
import typing

import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types

from . import column


def handle_object(
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
        The logical name, the SQLAlchemy column for the foreign key and the logical
        name and relationship for the reference to the object and the specification to
        record for the object reference.

    """
    obj_artifacts = gather_object_artifacts(
        spec=spec, logical_name=logical_name, schemas=schemas
    )

    # Handle object
    foreign_key_spec = handle_object_reference(
        spec=obj_artifacts.spec, schemas=schemas, fk_column=obj_artifacts.fk_column
    )
    return_value = column.handle_column(
        logical_name=f"{logical_name}_{obj_artifacts.fk_column}",
        spec=foreign_key_spec,
        required=required,
    )

    # Creating relationship
    backref = None
    if obj_artifacts.backref is not None:
        backref = sqlalchemy.orm.backref(
            obj_artifacts.backref, uselist=obj_artifacts.uselist
        )
    return_value.append(
        (
            logical_name,
            sqlalchemy.orm.relationship(
                obj_artifacts.ref_logical_name, backref=backref
            ),
        )
    )
    return return_value, {"type": "object", "x-de-$ref": obj_artifacts.ref_logical_name}


@dataclasses.dataclass
class ObjectArtifacts:
    """Artifacts retrieved from object schema."""

    spec: types.Schema
    ref_logical_name: str
    backref: typing.Optional[str]
    fk_column: str
    uselist: typing.Optional[bool]


def gather_object_artifacts(
    *, spec: types.Schema, logical_name: str, schemas: types.Schemas
) -> ObjectArtifacts:
    """
    Collect artifacts from a specification for constructing an object reference.

    Get the prepared specification, reference logical name, back reference and foreign
    key column name from a raw object specification.

    Raise MalformedRelationshipError if neither $ref nor $allOf is found.
    Raise MalformedRelationshipError if uselist is defined but backref is not.

    Args:
        spec: The schema for the column.
        schemas: Used to resolve any $ref.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The prepared specification, reference logical name, back reference and foreign
        key column.

    """
    # Default backref
    backref = None
    # Default uselist
    uselist = None
    # Initial foreign key column
    fk_column = None

    # Checking for $ref and allOf
    ref = spec.get("$ref")
    all_of = spec.get("allOf")

    if ref is not None:
        # Handle $ref
        ref_logical_name, spec = helpers.resolve_ref(
            name=logical_name, schema=spec, schemas=schemas
        )
    elif all_of is not None:
        # Checking for $ref, and x-backref and x-foreign-key-column counts
        _check_object_all_of(all_of_spec=all_of)

        # Handle allOf
        for sub_spec in all_of:
            backref = helpers.get_ext_prop(
                source=sub_spec, name="x-backref", default=backref
            )
            uselist = helpers.get_ext_prop(
                source=sub_spec, name="x-uselist", default=uselist
            )
            fk_column = helpers.get_ext_prop(
                source=sub_spec, name="x-foreign-key-column", default=fk_column
            )
            if sub_spec.get("$ref") is not None:
                ref_logical_name, spec = helpers.resolve_ref(
                    name=logical_name, schema=sub_spec, schemas=schemas
                )
    else:
        raise exceptions.MalformedRelationshipError(
            "Relationships are defined using either $ref or allOf."
        )

    # Resolving allOf
    spec = helpers.merge_all_of(schema=spec, schemas=schemas)

    # If backref has not been found look in referenced schema
    if backref is None:
        backref = helpers.get_ext_prop(source=spec, name="x-backref")
    # If uselist has not been found look in referenced schema
    if uselist is None:
        uselist = helpers.get_ext_prop(source=spec, name="x-uselist")
    # If foreign key column has not been found look in referenced schema
    if fk_column is None:
        fk_column = helpers.get_ext_prop(source=spec, name="x-foreign-key-column")
    # If foreign key column is still None, default to id
    if fk_column is None:
        fk_column = "id"

    # Check if uselist is defined and backref is not
    if uselist is not None and backref is None:
        raise exceptions.MalformedRelationshipError(
            "Relationships with x-uselist defined must also define x-backref."
        )

    return ObjectArtifacts(spec, ref_logical_name, backref, fk_column, uselist)


def _check_object_all_of(*, all_of_spec: types.AllOfSpec) -> None:
    """
    Check format of allOf for an object reference.

    Raise MalformedRelationshipError if the allOf schema is not as expected.

    Args:
        all_of_spec: The allOf specification to check.

    """
    # Checking for $ref and x-backref counts
    ref_count = 0
    backref_count = 0
    fk_column_count = 0
    uselist_count = 0
    for sub_spec in all_of_spec:
        if sub_spec.get("$ref") is not None:
            ref_count += 1
        if sub_spec.get("x-backref") is not None:
            backref_count += 1
        if sub_spec.get("x-foreign-key-column") is not None:
            fk_column_count += 1
        if sub_spec.get("x-uselist") is not None:
            uselist_count += 1
    if ref_count != 1:
        raise exceptions.MalformedRelationshipError(
            "Many to one relationships defined with allOf must have exactly one "
            "$ref in the allOf list."
        )
    if backref_count > 1:
        raise exceptions.MalformedRelationshipError(
            "Many to one relationships may have at most 1 x-backref defined."
        )
    if fk_column_count > 1:
        raise exceptions.MalformedRelationshipError(
            "Many to one relationships may have at most 1 x-foreign-key-column "
            "defined."
        )
    if uselist_count > 1:
        raise exceptions.MalformedRelationshipError(
            "Many to one relationships may have at most 1 x-uselist defined."
        )


def handle_object_reference(
    *, spec: types.Schema, schemas: types.Schemas, fk_column: str
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
