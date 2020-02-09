"""Functions relating to object references."""
# pylint: disable=useless-import-alias

import dataclasses
import typing

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy import types

from .. import column
from . import artifacts as artifacts
from . import foreign_key as foreign_key
from . import schema as _schema


def handle_object(
    *,
    schema: types.Schema,
    schemas: types.Schemas,
    required: typing.Optional[bool],
    logical_name: str,
    model_name: str,
    model_schema: types.Schema,
) -> typing.Tuple[
    typing.List[
        typing.Tuple[str, typing.Union[facades.sqlalchemy.column.Column, typing.Type]]
    ],
    types.ObjectRefSchema,
]:
    """
    Generate properties for a reference to another object.

    Assume that, when any $ref and allOf are resolved, the schema is an object.

    Args:
        schema: The schema for the column.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.
        logical_name: The logical name in the specification for the schema.
        model_schema: The schema of the model.

    Returns:
        The logical name, the SQLAlchemy column for the foreign key and the logical
        name and relationship for the reference to the object and the specification to
        record for the object reference.

    """
    # Retrieve artifacts required for object
    obj_artifacts = artifacts.gather(
        schema=schema, logical_name=logical_name, schemas=schemas
    )

    # Check for secondary
    if obj_artifacts.relationship.secondary is not None:
        raise exceptions.MalformedRelationshipError(
            "Many to one and one to one relationships do not support x-secondary."
        )

    # Record any backref
    helpers.backref.record(
        artifacts=obj_artifacts,
        ref_from_array=False,
        model_name=model_name,
        schemas=schemas,
    )

    # Construct foreign key
    fk_logical_name, fk_artifacts = foreign_key.gather_artifacts_helper(
        obj_artifacts=obj_artifacts, schemas=schemas, required=required
    )
    fk_required = foreign_key.check_required(
        artifacts=fk_artifacts,
        fk_logical_name=fk_logical_name,
        model_schema=model_schema,
        schemas=schemas,
    )
    if fk_required:
        fk_column = column.construct_column(artifacts=fk_artifacts)
        return_value = [(fk_logical_name, fk_column)]
    else:
        return_value = []

    return_schema = _schema.calculate(artifacts=obj_artifacts)
    # Create relationship
    relationship = facades.sqlalchemy.relationship(artifacts=obj_artifacts.relationship)
    return_value.append((logical_name, relationship))
    return (return_value, return_schema)
