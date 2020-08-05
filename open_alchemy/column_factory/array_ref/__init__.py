"""Functions relating to object references in arrays."""

import dataclasses
import typing

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy import types as oa_types

from ...utility_base import TOptUtilityBase
from .. import column
from .. import object_ref
from .. import types
from . import artifacts as _artifacts
from . import association_table as _association_table
from . import link as _link
from . import schema as _schema


def handle_array(
    *,
    schema: oa_types.Schema,
    model_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
    logical_name: str,
) -> typing.Tuple[types.TReturnValue, oa_types.ArrayRefSchema]:
    """
    Generate properties for a reference to another object through an array.

    Assume that when any allOf and $ref are resolved in the root spec the type is
    array.

    Args:
        schema: The schema for the column.
        model_schema: The schema of the parent.
        schemas: Used to resolve any $ref.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name and the relationship for the referenced object.

    """
    artifacts = _artifacts.gather(
        schema=schema, schemas=schemas, logical_name=logical_name
    )

    # Construct link between the models
    _link.construct(artifacts=artifacts, model_schema=model_schema, schemas=schemas)

    # Construct relationship
    relationship = facades.sqlalchemy.relationship(artifacts=artifacts.relationship)
    # Construct entry for the addition for the model schema
    return_schema = _schema.calculate(artifacts=artifacts)

    return [(logical_name, relationship)], return_schema
