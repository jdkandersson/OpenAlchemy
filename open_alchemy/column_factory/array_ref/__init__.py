"""Functions relating to object references in arrays."""

import dataclasses
import typing

import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy import types

from ...utility_base import TOptUtilityBase
from .. import column
from .. import object_ref
from . import artifacts as _artifacts
from . import association_table as _association_table
from . import schema as _schema
from . import set_foreign_key as _set_foreign_key


def handle_array(
    *,
    spec: types.Schema,
    model_schema: types.Schema,
    schemas: types.Schemas,
    logical_name: str,
) -> typing.Tuple[typing.List[typing.Tuple[str, typing.Type]], types.Schema]:
    """
    Generate properties for a reference to another object through an array.

    Assume that when any allOf and $ref are resolved in the root spec the type is
    array.

    Args:
        spec: The schema for the column.
        model_schema: The schema of the one to many parent.
        schemas: Used to resolve any $ref.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name and the relationship for the referenced object.

    """
    artifacts = _artifacts.gather(
        schema=spec, schemas=schemas, logical_name=logical_name
    )

    # Add foreign key to referenced schema
    if artifacts.relationship.secondary is None:
        _set_foreign_key.set_foreign_key(
            ref_model_name=artifacts.relationship.model_name,
            model_schema=model_schema,
            schemas=schemas,
            fk_column=artifacts.fk_column,
        )
    else:
        table = _association_table.construct(
            parent_schema=model_schema,
            child_schema=artifacts.spec,
            schemas=schemas,
            tablename=artifacts.relationship.secondary,
        )
        facades.models.set_association(
            table=table, name=artifacts.relationship.secondary
        )

    # Construct relationship
    relationship = facades.sqlalchemy.relationship(artifacts=artifacts.relationship)
    # Construct entry for the addition for the model schema
    return_schema = _schema.calculate(artifacts=artifacts)

    return [(logical_name, relationship)], return_schema
