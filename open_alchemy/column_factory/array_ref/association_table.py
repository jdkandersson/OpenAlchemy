"""Construct secondary table."""

import dataclasses
import typing

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy import types

from .. import column


@dataclasses.dataclass
class _ColumnArtifacts:
    """Artifacts for constructing a many to many column of a secondary table."""

    # The type of the column
    type: str
    # The format of the column
    format: typing.Optional[str]
    # The table name with the foreign key
    tablename: str
    # The column name for the foreign key
    column_name: str
    # The max length of the column
    max_length: typing.Optional[int]


def _gather_column_artifacts(
    *, model_schema: types.Schema, schemas: types.Schemas
) -> _ColumnArtifacts:
    """
    Retrieve column artifacts of a secondary table for a many to many relationship.

    The model primary key is used as the base of the foreign key column in the
    secondary table for the model. It is assumed that the model has a single primary key
    column.

    Raise MalformedSchemaError if the model schema does not have a type, has a type but
    is not an object, does not have the x-tablename property, does not have any
    properties, does not have exactly 1 primary key, the primary key column doesn't
    define a type or the type is an object or array.

    Args:
        model_schema: The schema for one side of the many to many relationship.
        schemas: Used to resolve any $ref.

    Returns:
        The artifacts needed to construct a column of the secondary table in a many to
        many relationship.

    """
    # Resolve $ref and merge allOf
    model_schema = helpers.schema.prepare(schema=model_schema, schemas=schemas)

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
    tablename = helpers.ext_prop.get(source=model_schema, name="x-tablename")
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
            # Check whether this is the first primary key that has been encountered
            if type_ is not None:
                raise exceptions.MalformedSchemaError(
                    "A schema that is part of a many to many relationship must have "
                    "exactly 1 primary key."
                )

            # Gather artifacts for constructing the foreign key column
            try:
                type_ = helpers.peek.type_(schema=property_schema, schemas=schemas)
            except exceptions.TypeMissingError as exc:
                raise exceptions.MalformedSchemaError(
                    "A schema that is part of a many to many relationship must define "
                    "a type for the primary key."
                ) from exc
            format_ = helpers.peek.format_(schema=property_schema, schemas=schemas)
            max_length = helpers.peek.max_length(
                schema=property_schema, schemas=schemas
            )
            column_name = property_name

    # Check whether at least 1 primary key column has been found
    if type_ is None:
        raise exceptions.MalformedSchemaError(
            "A schema that is part of a many to many relationship must have "
            "exactly 1 primary key."
        )
    # Check that the type is for a column
    if type_ in {"object", "array"}:
        raise exceptions.MalformedSchemaError(
            "A schema that is part of a many to many relationship cannot define it's "
            "primary key to be of type object nor array."
        )

    return _ColumnArtifacts(
        type=type_,
        format=format_,
        tablename=tablename,
        column_name=column_name,
        max_length=max_length,
    )


def _construct_column(
    *, artifacts: _ColumnArtifacts
) -> facades.sqlalchemy.column.Column:
    """
    Construct many to many column.

    Take the artifacts gathered for a foreign key reference for an association table
    and construct the corresponding column.

    Args:
        artifacts: The artifacts based on which to construct the column

    Returns:
        The column.

    """
    # Convert to column artifacts
    column_artifacts = types.ColumnArtifacts(
        open_api=types.OpenAPiColumnArtifacts(
            type=artifacts.type,
            format=artifacts.format,
            max_length=artifacts.max_length,
        ),
        extension=types.ExtensionColumnArtifacts(
            foreign_key=f"{artifacts.tablename}.{artifacts.column_name}"
        ),
    )

    # Construct column
    return_column = column.construct_column(artifacts=column_artifacts)
    # Set column name for the table
    return_column.name = f"{artifacts.tablename}_{artifacts.column_name}"

    return return_column


def construct(
    *,
    parent_schema: types.Schema,
    child_schema: types.Schema,
    schemas: types.Schemas,
    tablename: str,
) -> facades.sqlalchemy.Table:
    """
    Construct many to many association table.

    Gather artifacts for both models, construct foreign key column for models and
    combine into a table.

    Args:
        parent_schema: The schema for the many to many parent.
        child_schema: The schema for the many to many child.
        schemas: Used to resolve any $ref.
        tablename: The name of the association table.

    Returns:
        The association table.

    """
    # Gather artifacts for parent and child model
    parent_artifacts = _gather_column_artifacts(
        model_schema=parent_schema, schemas=schemas
    )
    child_artifacts = _gather_column_artifacts(
        model_schema=child_schema, schemas=schemas
    )

    # Construct columns for parent and child models
    parent_column = _construct_column(artifacts=parent_artifacts)
    child_column = _construct_column(artifacts=child_artifacts)

    # Construct table
    base = facades.models.get_base()
    return facades.sqlalchemy.table(
        tablename=tablename, base=base, columns=(parent_column, child_column)
    )
