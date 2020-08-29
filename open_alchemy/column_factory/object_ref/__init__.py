"""Functions relating to object references."""
# pylint: disable=useless-import-alias

import dataclasses
import typing

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy import types as oa_types

from .. import column
from .. import types
from . import artifacts as artifacts
from . import schema as _schema


def handle_object(
    *,
    schema: oa_types.Schema,
    schemas: oa_types.Schemas,
    logical_name: str,
) -> typing.Tuple[types.TReturnValue, oa_types.ObjectRefSchema]:
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

    return_schema = _schema.calculate(artifacts=obj_artifacts)
    # Create relationship
    relationship = facades.sqlalchemy.relationship(artifacts=obj_artifacts.relationship)
    return ([(logical_name, relationship)], return_schema)
