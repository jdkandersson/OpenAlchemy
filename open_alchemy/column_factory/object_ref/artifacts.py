"""Functions for object reference artifacts."""

import dataclasses
import typing

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types


def gather(
    *, schema: types.Schema, logical_name: str, schemas: types.Schemas
) -> types.ObjectArtifacts:
    """
    Collect artifacts from a specification for constructing an object reference.

    Get the prepared specification, reference logical name, back reference and foreign
    key column name from a raw object specification.

    Raise MalformedRelationshipError if neither $ref nor $allOf is found.
    Raise MalformedRelationshipError if uselist is defined but backref is not.
    Raise MalformedRelationshipError if multiple $ref, x-backref, x-secondary,
    x-foreign-key-column or x-uselist are found.

    Args:
        schema: The schema for the column.
        schemas: Used to resolve any $ref.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The prepared specification, reference logical name, back reference and foreign
        key column.

    """
    intermediary_obj_artifacts = _handle_schema(
        logical_name=logical_name, schema=schema, schemas=schemas
    )

    # Check if uselist is defined and backref is not
    if (
        intermediary_obj_artifacts.uselist is not None
        and intermediary_obj_artifacts.backref is None
    ):
        raise exceptions.MalformedRelationshipError(
            "Relationships with x-uselist defined must also define x-backref."
        )

    # Construct back reference
    back_reference = None
    if intermediary_obj_artifacts.backref is not None:
        back_reference = types.BackReferenceArtifacts(
            property_name=intermediary_obj_artifacts.backref,
            uselist=intermediary_obj_artifacts.uselist,
        )

    return types.ObjectArtifacts(
        spec=intermediary_obj_artifacts.ref_schema,
        logical_name=logical_name,
        fk_column=intermediary_obj_artifacts.fk_column_name,
        relationship=types.RelationshipArtifacts(
            model_name=intermediary_obj_artifacts.ref_model_name,
            back_reference=back_reference,
            secondary=intermediary_obj_artifacts.secondary,
            kwargs=intermediary_obj_artifacts.kwargs,
        ),
        nullable=intermediary_obj_artifacts.nullable,
        description=intermediary_obj_artifacts.description,
        write_only=intermediary_obj_artifacts.write_only,
    )


@dataclasses.dataclass
class _IntermediaryObjectArtifacts:
    """Object artifacts before foreign key column artifacts are gathered."""

    # The name of the referenced model
    ref_model_name: str
    # The name of the foreign key column
    fk_column_name: str
    # The schema for the foreign key column
    ref_schema: types.Schema
    # The back reference for the relationship
    backref: typing.Optional[str] = None
    # Whether to use a list for the back reference
    uselist: typing.Optional[bool] = None
    # The name of the secondary table to use for the relationship
    secondary: typing.Optional[str] = None
    # Whether the foreign key is nullable
    nullable: typing.Optional[bool] = None
    # The description for the reference
    description: typing.Optional[str] = None
    # The write_only for the reference
    write_only: typing.Optional[bool] = None
    # Keyword arguments for relationship construction
    kwargs: types.TOptKwargs = None


def _handle_schema(
    *, logical_name: str, schema: types.Schema, schemas: types.Schemas
) -> _IntermediaryObjectArtifacts:
    """
    Gather artifacts from the schema.

    Args:
        schema: The schema of the object reference.
        logical_name: The property name of the object reference.
        schemas: Used to resolve any $ref.

    Returns:
        The name of the referenced schema.

    """
    # Read $ref and allOf
    ref = schema.get("$ref")
    all_of = schema.get("allOf")

    if ref is not None:
        intermediary_obj_artifacts = _handle_ref(
            logical_name=logical_name, schema=schema, schemas=schemas
        )
    elif all_of is not None:
        intermediary_obj_artifacts = _handle_all_of(
            logical_name=logical_name, all_of_schema=all_of, schemas=schemas
        )
    else:
        raise exceptions.MalformedRelationshipError(
            "Relationships are defined using either $ref or allOf."
        )

    return intermediary_obj_artifacts


def _handle_ref(
    *, logical_name: str, schema: types.Schema, schemas: types.Schemas
) -> _IntermediaryObjectArtifacts:
    """
    Gather artifacts from a $ref.

    Args:
        schema: The schema of the object reference.
        logical_name: The property name of the object reference.
        schemas: Used to resolve any $ref.

    Returns:
        The name of the referenced schema.

    """
    ref_model_name, ref_schema = helpers.ref.resolve(
        name=logical_name, schema=schema, schemas=schemas
    )
    ref_schema = helpers.all_of.merge(schema=ref_schema, schemas=schemas)

    # Check referenced schema
    try:
        type_ = helpers.peek.type_(schema=ref_schema, schemas=schemas)
    except exceptions.TypeMissingError as exc:
        raise exceptions.MalformedRelationshipError(
            "The referenced schema does not have a type."
        ) from exc
    if type_ != "object":
        raise exceptions.MalformedRelationshipError(
            "A reference in a relationship must resolve to an object."
        )

    # Read other parameters
    backref = helpers.ext_prop.get(source=ref_schema, name="x-backref")
    uselist = helpers.ext_prop.get(source=ref_schema, name="x-uselist")
    secondary = helpers.ext_prop.get(source=ref_schema, name="x-secondary")
    fk_column_name = helpers.ext_prop.get(
        source=ref_schema, name="x-foreign-key-column"
    )
    if fk_column_name is None:
        fk_column_name = "id"
    nullable = helpers.peek.nullable(schema=ref_schema, schemas={})
    write_only = helpers.peek.write_only(schema=ref_schema, schemas={})

    return _IntermediaryObjectArtifacts(
        ref_model_name=ref_model_name,
        fk_column_name=fk_column_name,
        ref_schema=ref_schema,
        backref=backref,
        uselist=uselist,
        secondary=secondary,
        nullable=nullable,
        write_only=write_only,
    )


def _handle_all_of(
    *,
    logical_name: str,
    all_of_schema: typing.List[types.Schema],
    schemas: types.Schemas,
) -> _IntermediaryObjectArtifacts:
    """
    Gather artifacts from a allOf.

    Raise MalformedRelationshipError if there are no or multiple $ref in the allOf list.

    Args:
        schema: The schema of the object reference.
        logical_name: The property name of the object reference.
        schemas: Used to resolve any $ref.

    Returns:
        The name of the referenced schema.

    """
    # Initial values
    obj_artifacts: typing.Optional[_IntermediaryObjectArtifacts] = None
    secondary: typing.Optional[str] = None
    backref: typing.Optional[str] = None
    uselist: typing.Optional[bool] = None
    fk_column_name: typing.Optional[str] = None
    nullable: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    write_only: typing.Optional[bool] = None
    kwargs: types.TOptKwargs = None

    # Exceptions with their messages
    incorrect_number_of_ref = exceptions.MalformedRelationshipError(
        "Relationships defined with allOf must have exactly one $ref in the allOf "
        "list."
    )

    for sub_schema in all_of_schema:
        # Handle $ref
        if sub_schema.get("$ref") is not None:
            # Check whether $ref was already found
            if obj_artifacts is not None:
                raise incorrect_number_of_ref

            obj_artifacts = _handle_ref(
                logical_name=logical_name, schema=sub_schema, schemas=schemas
            )

        # Handle backref
        backref = _handle_key_single(
            key="x-backref",
            schema=sub_schema,
            default=backref,
            exception_message="Relationships may have at most 1 x-backref defined.",
        )
        # Handle uselist
        uselist = _handle_key_single(
            key="x-uselist",
            schema=sub_schema,
            default=uselist,
            exception_message="Relationships may have at most 1 x-uselist defined.",
        )
        # Handle secondary
        secondary = _handle_key_single(
            key="x-secondary",
            schema=sub_schema,
            default=secondary,
            exception_message="Relationships may have at most 1 x-secondary defined.",
        )
        # Handle fk_column_name
        fk_column_name = _handle_key_single(
            key="x-foreign-key-column",
            schema=sub_schema,
            default=fk_column_name,
            exception_message=(
                "Relationships may have at most 1 x-foreign-key-column defined."
            ),
        )
        # Handle nullable
        nullable = _handle_key_single(
            key="nullable",
            schema=sub_schema,
            default=nullable,
            exception_message="Relationships may have at most 1 nullable defined.",
        )
        # Handle description
        description = _handle_key_single(
            key="description",
            schema=sub_schema,
            default=description,
            exception_message="Relationships may have at most 1 description defined.",
        )
        # Handle writeOnly
        write_only = _handle_key_single(
            key="writeOnly",
            schema=sub_schema,
            default=write_only,
            exception_message="Relationships may have at most 1 writeOnly defined.",
        )
        # Handle kwargs
        kwargs = _handle_key_single(
            key="x-kwargs",
            schema=sub_schema,
            default=kwargs,
            exception_message="Relationships may have at most 1 x-kwargs defined.",
        )

    # Check that $ref was found once
    if obj_artifacts is None:
        raise incorrect_number_of_ref
    if backref is not None:
        obj_artifacts.backref = backref
    if uselist is not None:
        obj_artifacts.uselist = uselist
    if secondary is not None:
        obj_artifacts.secondary = secondary
    if fk_column_name is not None:
        obj_artifacts.fk_column_name = fk_column_name
    if nullable is not None:
        obj_artifacts.nullable = nullable
    if description is not None:
        obj_artifacts.description = description
    if write_only is not None:
        obj_artifacts.write_only = write_only
    if kwargs is not None:
        obj_artifacts.kwargs = kwargs

    return obj_artifacts


_TValue = typing.TypeVar("_TValue")


def _handle_key_single(
    *, key: str, schema: types.Schema, default: _TValue, exception_message: str
) -> _TValue:
    """
    Read value and enforce that it only exists once.

    Raise MalformedRelationshipError is default is not None and the key exists in the
        schema.

    ARgs:
        key: The key to read the value of.
        schema: The schema to read the value from.
        default: The default value to return.
        exception_message: The message raised with the exception.

    Returns:
        The value of the key or the default value,

    """
    if key.startswith("x-"):
        if key == "x-kwargs":
            sub_value = helpers.ext_prop.get_kwargs(
                source=schema, reserved={"backref", "secondary"}
            )
        else:
            sub_value = helpers.ext_prop.get(source=schema, name=key)
    else:
        sub_value = schema.get(key)
    if sub_value is not None:
        if default is not None:
            raise exceptions.MalformedRelationshipError(exception_message)

        return sub_value
    return default
