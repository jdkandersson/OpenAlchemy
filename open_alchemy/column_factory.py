"""Generate columns based on OpenAPI schema property."""

import re
import typing

import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


def column_factory(
    *,
    spec: types.Schema,
    schemas: types.Schemas,
    required: typing.Optional[bool] = None,
    logical_name: str,
) -> typing.List[typing.Tuple[str, sqlalchemy.Column]]:
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
        return _handle_column(logical_name=logical_name, spec=spec, required=required)

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
) -> typing.List[typing.Tuple[str, typing.Union[sqlalchemy.Column, typing.Type]]]:
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
        # Checking for $ref and x-backref counts
        ref_count = 0
        backref_count = 0
        for sub_spec in all_of:
            if sub_spec.get("$ref") is not None:
                ref_count += 1
            if sub_spec.get("x-backref") is not None:
                backref_count += 1
        if ref_count != 1:
            raise exceptions.MalformedManyToOneRelationshipError(
                "Many to One relationships defined with allOf must have exactly one "
                "$ref in the allOf list."
            )
        if backref_count > 1:
            raise exceptions.MalformedManyToOneRelationshipError(
                "Many to One relationships may have at most 1 x-backref defined."
            )

        # Handling allOf
        for sub_spec in all_of:
            backref = helpers.get_ext_prop(source=sub_spec, name="x-backref")
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

    # Handling object
    foreign_key_spec = _handle_object_reference(spec=spec, schemas=schemas)
    return_value = _handle_column(
        logical_name=f"{logical_name}_id", spec=foreign_key_spec, required=required
    )

    # Creating relationship
    return_value.append(
        (logical_name, sqlalchemy.orm.relationship(ref_logical_name, backref=backref))
    )
    return return_value


def _handle_column(
    *, spec: types.Schema, required: typing.Optional[bool] = None, logical_name: str
) -> typing.List[typing.Tuple[str, sqlalchemy.Column]]:
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
    # Generating the SQLAlchemy column
    column = _spec_to_column(spec=spec, required=required)
    # Adding the logical name
    return [(logical_name, column)]


def _spec_to_column(*, spec: types.Schema, required: typing.Optional[bool] = None):
    """
    Convert specification to a SQLAlchemy column.

    Args:
        spec: The schema for the column.
        required: Whether the object property is required.

    Returns:
        The SQLAlchemy column based on the schema.

    """
    # Keep track of column arguments
    args: typing.Tuple[typing.Any, ...] = ()
    kwargs: types.Schema = {}

    # Calculate column modifiers
    kwargs["nullable"] = _calculate_nullable(spec=spec, required=required)
    if helpers.get_ext_prop(source=spec, name="x-primary-key"):
        kwargs["primary_key"] = True
    autoincrement = helpers.get_ext_prop(source=spec, name="x-autoincrement")
    if autoincrement is not None:
        if autoincrement:
            kwargs["autoincrement"] = True
        else:
            kwargs["autoincrement"] = False
    if helpers.get_ext_prop(source=spec, name="x-index"):
        kwargs["index"] = True
    if helpers.get_ext_prop(source=spec, name="x-unique"):
        kwargs["unique"] = True
    foreign_key = helpers.get_ext_prop(source=spec, name="x-foreign-key")
    if foreign_key:
        args = (*args, sqlalchemy.ForeignKey(foreign_key))

    # Calculating type of column
    type_ = _determine_type(spec=spec)

    return sqlalchemy.Column(type_, *args, **kwargs)


def _handle_object_reference(
    *, spec: types.Schema, schemas: types.Schemas
) -> types.Schema:
    """
    Determine the foreign key schema for an object reference.

    Args:
        spec: The schema of the object reference.
        schemas: All defined schemas.

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
    logical_name = "id"
    id_spec = properties.get(logical_name)
    if id_spec is None:
        raise exceptions.MalformedSchemaError(
            "Referenced object does not have id property."
        )
    # Preparing specification
    prepared_id_spec = helpers.prepare_schema(schema=id_spec, schemas=schemas)
    id_type = prepared_id_spec.get("type")
    if id_type is None:
        raise exceptions.MalformedSchemaError(
            "Referenced object id property does not have a type."
        )

    return {"type": id_type, "x-foreign-key": f"{tablename}.id"}


def _calculate_nullable(*, spec: types.Schema, required: typing.Optional[bool]) -> bool:
    """
    Calculate the value of the nullable field.

    The following is the truth table for the nullable property.
    required  | schema nullable | returned nullable
    --------------------------------------------------------
    None      | not given       | True
    None      | False           | False
    None      | True            | True
    False     | not given       | True
    False     | False           | False
    False     | True            | True
    True      | not given       | False
    True      | False           | False
    True      | True            | True

    To summarize, if nullable is the schema the value for it is used. Otherwise True
    is returned unless required is True.

    Args:
        spec: The schema for the column.
        required: Whether the property is required.

    Returns:
        The nullable value for the column.

    """
    nullable = spec.get("nullable")
    if nullable is None:
        if required:
            return False
        return True
    if nullable:
        return True
    return False


def _determine_type(*, spec: types.Schema) -> sqlalchemy.sql.type_api.TypeEngine:
    """
    Determine the type for a specification.

    If no type is found, raises TypeMissingError. If the type is found but is not
    handled, raises FeatureNotImplementedError.

    Args:
        spec: The specification to determine the type for.

    Returns:
        The type for the specification.

    """
    # Checking for type
    spec_type = spec.get("type")
    if spec_type is None:
        raise exceptions.TypeMissingError("Every property requires a type.")

    # Determining the type
    type_: typing.Optional[sqlalchemy.sql.type_api.TypeEngine] = None
    if spec_type == "integer":
        type_ = _handle_integer(spec=spec)
    elif spec_type == "number":
        type_ = _handle_number(spec=spec)
    elif spec_type == "string":
        type_ = _handle_string(spec=spec)
    elif spec_type == "boolean":
        type_ = sqlalchemy.Boolean

    if type_ is None:
        raise exceptions.FeatureNotImplementedError(
            f"{spec['type']} has not been implemented"
        )
    return type_


def _handle_integer(
    *, spec: types.Schema
) -> typing.Union[sqlalchemy.Integer, sqlalchemy.BigInteger]:
    """
    Determine the type of integer to use for the schema.

    Args:
        spec: The schema for the integer column.

    Returns:
        Integer or BigInteger depending on the format.

    """
    if spec.get("format", "int32") == "int32":
        return sqlalchemy.Integer
    if spec.get("format") == "int64":
        return sqlalchemy.BigInteger
    raise exceptions.FeatureNotImplementedError(
        f"{spec.get('format')} format for integer is not supported."
    )


def _handle_number(*, spec: types.Schema) -> sqlalchemy.Float:
    """
    Determine the type of number to use for the schema.

    Args:
        spec: The schema for the number column.

    Returns:
        Float.

    """
    if spec.get("format", "float") == "float":
        return sqlalchemy.Float
    raise exceptions.FeatureNotImplementedError(
        f"{spec.get('format')} format for number is not supported."
    )


def _handle_string(*, spec: types.Schema) -> sqlalchemy.String:
    """
    Determine the setup of the string to use for the schema.

    Args:
        spec: The schema for the string column.

    Returns:
        String.

    """
    return sqlalchemy.String(length=spec.get("maxLength"))
