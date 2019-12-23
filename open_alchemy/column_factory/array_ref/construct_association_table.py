"""Construct secondary table."""

import dataclasses
import typing

import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy import types

from .. import column


@dataclasses.dataclass
class _ManyToManyColumnArtifacts:
    """Artifacts for constructing a many to many column of a secondary table."""

    type_: str
    format_: typing.Optional[str]
    tablename: str
    column_name: str
    max_length: typing.Optional[int]


def _many_to_many_column_artifacts(
    *, model_schema: types.Schema, schemas: types.Schemas
) -> _ManyToManyColumnArtifacts:
    """
    Retrieve column artifacts of a secondary table for a many to many relationship.

    Args:
        model_schema: The schema for one side of the many to many relationship.
        schemas: Used to resolve any $ref.

    Returns:
        The artifacts needed to construct a column of the secondary table in a many to
        many relationship.

    """
    # Resolve $ref and merge allOf
    model_schema = helpers.prepare_schema(schema=model_schema, schemas=schemas)

    # Check schema type
    model_type = model_schema.get("type")
    if model_type is None:
        raise exceptions.MalformedSchemaError("Every schema must have a type.")
    if model_type != "object":
        raise exceptions.MalformedSchemaError(
            "A schema that is part of a many to many relationship must be of type "
            "object."
        )

    # Retrieve table name
    tablename = helpers.get_ext_prop(source=model_schema, name="x-tablename")
    if tablename is None:
        raise exceptions.MalformedSchemaError(
            "A schema that is part of a many to many relationship must set the "
            "x-tablename property."
        )

    # Find primary key
    properties = model_schema.get("properties")
    if properties is None:
        raise exceptions.MalformedSchemaError(
            "A schema that is part of a many to many relationship must have properties."
        )
    if not properties:
        raise exceptions.MalformedSchemaError(
            "A schema that is part of a many to many relationship must have at least 1 "
            "property."
        )
    type_ = None
    format_ = None
    for property_name, property_schema in properties.items():
        if helpers.peek.primary_key(schema=property_schema, schemas=schemas):
            if type_ is not None:
                raise exceptions.MalformedSchemaError(
                    "A schema that is part of a many to many relationship must have "
                    "exactly 1 primary key."
                )
            try:
                type_ = helpers.peek.type_(schema=property_schema, schemas=schemas)
            except exceptions.TypeMissingError:
                raise exceptions.MalformedSchemaError(
                    "A schema that is part of a many to many relationship must define "
                    "a type for the primary key."
                )
            format_ = helpers.peek.format_(schema=property_schema, schemas=schemas)
            max_length = helpers.peek.max_length(
                schema=property_schema, schemas=schemas
            )
            column_name = property_name
    if type_ is None:
        raise exceptions.MalformedSchemaError(
            "A schema that is part of a many to many relationship must have "
            "exactly 1 primary key."
        )
    if type_ in {"object", "array"}:
        raise exceptions.MalformedSchemaError(
            "A schema that is part of a many to many relationship cannot define it's "
            "primary key to be of type object nor array."
        )

    return _ManyToManyColumnArtifacts(
        type_, format_, tablename, column_name, max_length
    )


def _many_to_many_column(*, artifacts: _ManyToManyColumnArtifacts) -> sqlalchemy.Column:
    """
    Construct many to many column.

    Args:
        artifacts: The artifacts based on which to construct the column

    Returns:
        The column.

    """
    spec: types.Schema = {
        "type": artifacts.type_,
        "x-foreign-key": f"{artifacts.tablename}.{artifacts.column_name}",
    }
    if artifacts.format_ is not None:
        spec["format"] = artifacts.format_
    if artifacts.max_length is not None:
        spec["maxLength"] = artifacts.max_length
    _, return_column = column.handle_column(schema=spec)
    return_column.name = f"{artifacts.tablename}_{artifacts.column_name}"
    return return_column


def construct_association_table(
    *,
    parent_schema: types.Schema,
    child_schema: types.Schema,
    schemas: types.Schemas,
    tablename: str,
) -> sqlalchemy.Table:
    """
    Construct many to many association table.

    Args:
        parent_schema: The schema for the many to many parent.
        child_schema: The schema for the many to many child.
        schemas: Used to resolve any $ref.
        tablename: The name of the association table.

    Returns:
        The association table.

    """
    parent_artifacts = _many_to_many_column_artifacts(
        model_schema=parent_schema, schemas=schemas
    )
    child_artifacts = _many_to_many_column_artifacts(
        model_schema=child_schema, schemas=schemas
    )
    parent_column = _many_to_many_column(artifacts=parent_artifacts)
    child_column = _many_to_many_column(artifacts=child_artifacts)
    base = facades.models.get_base()
    return sqlalchemy.Table(tablename, base.metadata, parent_column, child_column)
