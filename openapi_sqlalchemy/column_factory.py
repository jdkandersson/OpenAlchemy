"""Generate columns based on openapi schema property."""

import re
import typing

import sqlalchemy

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import helpers
from openapi_sqlalchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


@helpers.testing_guard(environment_name="TESTING")
def resolve_ref(func: typing.Callable) -> typing.Callable:
    """Resolve $ref schemas."""

    def inner(
        *, spec: types.SchemaSpec, schemas: types.Schemas, logical_name: str, **kwargs
    ) -> sqlalchemy.Column:
        """Replace function."""
        # Resolveing any $ref
        schema = types.Schema(logical_name=logical_name, spec=spec)
        ref_schema = helpers.resolve_ref(schema=schema, schemas=schemas)

        # Checking for type
        type_ = ref_schema.spec.get("type")
        if type_ != "object":
            return func(
                logical_name=logical_name,
                spec=ref_schema.spec,
                schemas=schemas,
                **kwargs,
            )

        # Handling object
        foreign_key_spec = _handle_object(spec=ref_schema.spec, schemas=schemas)
        return_value = func(
            logical_name=f"{logical_name}_id",
            spec=foreign_key_spec,
            schemas=schemas,
            **kwargs,
        )

        # Creating relationship
        return_value.append(
            (logical_name, sqlalchemy.orm.relationship(ref_schema.logical_name))
        )
        return return_value

    return inner


@helpers.testing_guard(environment_name="TESTING")
def merge_all_of(func: typing.Callable) -> typing.Callable:
    """Merge allOf specification."""

    def inner(
        *, spec: types.SchemaSpec, schemas: types.Schemas, **kwargs
    ) -> sqlalchemy.Column:
        """Replace function."""
        merged_spec = helpers.merge_all_of(spec=spec, schemas=schemas)
        return func(spec=merged_spec, **kwargs)

    return inner


@resolve_ref
@helpers.add_logical_name
@merge_all_of
def column_factory(
    *, spec: types.SchemaSpec, required: typing.Optional[bool] = None
) -> sqlalchemy.Column:
    """
    Generate column based on openapi schema property.

    Args:
        spec: The schema for the column.
        required: Whether the object property is required.

    Returns:
        The SQLAlchemy column based on the schema.

    """
    # Keep track of column arguments
    args: typing.Tuple[typing.Any, ...] = ()
    kwargs: typing.Dict[str, typing.Any] = {}

    # Calculate column modifiers
    kwargs["nullable"] = _calculate_nullable(spec=spec, required=required)
    if spec.get("x-primary-key"):
        kwargs["primary_key"] = True
    autoincrement = spec.get("x-autoincrement")
    if autoincrement is not None:
        if autoincrement:
            kwargs["autoincrement"] = True
        else:
            kwargs["autoincrement"] = False
    if spec.get("x-index"):
        kwargs["index"] = True
    if spec.get("x-unique"):
        kwargs["unique"] = True
    if spec.get("x-foreign-key"):
        args = (*args, sqlalchemy.ForeignKey(spec.get("x-foreign-key")))

    # Calculating type of column
    type_ = _determine_type(spec=spec)

    return sqlalchemy.Column(type_, *args, **kwargs)


def _handle_object(
    *, spec: types.SchemaSpec, schemas: types.Schemas
) -> types.SchemaSpec:
    """
    Determine the foreign key schema for an object reference.

    Args:
        spec: The schema of the object reference.
        schemas: All defined schemas.

    Returns:
        The foreign key schema.

    """
    tablename = spec.get("x-tablename")
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
    prepared_id_spec = helpers.prepare_spec(spec=id_spec, schemas=schemas)
    id_type = prepared_id_spec.get("type")
    if id_type is None:
        raise exceptions.MalformedSchemaError(
            "Referenced object id property does not have a type."
        )

    return {"type": id_type, "x-foreign-key": f"{tablename}.id"}


def _calculate_nullable(
    *, spec: types.SchemaSpec, required: typing.Optional[bool]
) -> bool:
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


def _determine_type(*, spec: types.SchemaSpec) -> sqlalchemy.sql.type_api.TypeEngine:
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
    *, spec: types.SchemaSpec
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


def _handle_number(*, spec: types.SchemaSpec) -> sqlalchemy.Float:
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


def _handle_string(*, spec: types.SchemaSpec) -> sqlalchemy.String:
    """
    Determine the setup of the string to use for the schema.

    Args:
        spec: The schema for the string column.

    Returns:
        String.

    """
    return sqlalchemy.String(length=spec.get("maxLength"))
