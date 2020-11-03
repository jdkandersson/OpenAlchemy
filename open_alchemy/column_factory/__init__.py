"""Generate columns based on OpenAPI schema property."""

import typing

from open_alchemy import helpers
from open_alchemy import types as oa_types
from open_alchemy.schemas.artifacts import property_

from . import backref
from . import json
from . import relationship
from . import simple
from . import types

_TReturnSchema = typing.Union[
    oa_types.ColumnSchema,
    oa_types.ObjectRefSchema,
    oa_types.ArrayRefSchema,
    oa_types.Schema,
]


def column_factory(
    *,
    schema: oa_types.Schema,
    model_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
    required: typing.Optional[bool] = None,
    logical_name: str,
) -> typing.Tuple[types.TReturnValue, _TReturnSchema]:
    """
    Generate column based on OpenAPI schema property.

    Args:
        schema: The schema for the column.
        model_schema: The schema of the model.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name, the SQLAlchemy column based on the schema and the
        specification to store for the column.

    """
    artifacts = property_.get(
        schemas=schemas,
        model_schema=model_schema,
        property_name=logical_name,
        schema=schema,
        required=required is True,
    )
    if artifacts.type == helpers.property_.Type.SIMPLE:
        simple_column_value, simple_column_schema = simple.handle(artifacts=artifacts)
        return ([(logical_name, simple_column_value)], simple_column_schema)
    if artifacts.type == helpers.property_.Type.JSON:
        json_column_value, json_column_schema = json.handle(artifacts=artifacts)
        return ([(logical_name, json_column_value)], json_column_schema)
    if artifacts.type == helpers.property_.Type.BACKREF:
        return backref.handle(artifacts=artifacts)
    return relationship.handle(artifacts=artifacts, logical_name=logical_name)
