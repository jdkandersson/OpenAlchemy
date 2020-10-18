"""Functions relating to object references in arrays."""

import typing

from open_alchemy import facades
from open_alchemy import types as oa_types

from ...utility_base import TOptUtilityBase
from .. import types
from . import artifacts as _artifacts
from . import schema as _schema


def handle_array(
    *,
    schema: oa_types.Schema,
    schemas: oa_types.Schemas,
    logical_name: str,
) -> typing.Tuple[types.TReturnValue, oa_types.ArrayRefSchema]:
    """
    Generate properties for a reference to another object through an array.

    Assume that when any allOf and $ref are resolved in the root spec the type is
    array.

    Args:
        schema: The schema for the column.
        schemas: Used to resolve any $ref.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name and the relationship for the referenced object.

    """
    artifacts = _artifacts.gather(
        schema=schema, schemas=schemas, logical_name=logical_name
    )

    # Construct relationship
    relationship = facades.sqlalchemy.relationship(artifacts=artifacts.relationship)
    # Construct entry for the addition for the model schema
    return_schema = _schema.calculate(artifacts=artifacts)

    return [(logical_name, relationship)], return_schema
