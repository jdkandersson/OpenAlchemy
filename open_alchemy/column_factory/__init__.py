"""Generate columns based on OpenAPI schema property."""

import re
import typing

from open_alchemy import helpers
from open_alchemy import types as oa_types
from open_alchemy.schemas.artifacts import property_

from . import array_ref
from . import backref
from . import column
from . import json
from . import object_ref
from . import read_only
from . import relationship
from . import simple
from . import types

_TReturnSchema = typing.Union[
    oa_types.ColumnSchema,
    oa_types.ObjectRefSchema,
    oa_types.ArrayRefSchema,
    oa_types.ReadOnlySchema,
]


def old_column_factory(
    *,
    schema: oa_types.Schema,
    schemas: oa_types.Schemas,
    required: typing.Optional[bool] = None,
    logical_name: str,
) -> typing.Tuple[types.TReturnValue, _TReturnSchema]:
    """
    Generate column based on OpenAPI schema property.

    Args:
        schema: The schema for the column.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name, the SQLAlchemy column based on the schema and the
        specification to store for the column.

    """
    # Check type
    type_ = helpers.peek.type_(schema=schema, schemas=schemas)

    if type_ not in {"object", "array"} or helpers.peek.json(
        schema=schema, schemas=schemas
    ):
        column_value, column_schema = column.handle_column(
            schema=schema, schemas=schemas, required=required
        )
        return ([(logical_name, column_value)], column_schema)

    # Check readOnly
    if helpers.peek.read_only(schema=schema, schemas=schemas):
        return read_only.handle_read_only(schema=schema, schemas=schemas)

    if type_ == "object":
        # Handle objects
        return object_ref.handle_object(
            schema=schema,
            schemas=schemas,
            logical_name=logical_name,
        )

    # Handle arrays
    return array_ref.handle_array(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
    )


# def column_factory(
#     *,
#     schema: oa_types.Schema,
#     model_schema: oa_types.Schema,
#     schemas: oa_types.Schemas,
#     required: typing.Optional[bool] = None,
#     logical_name: str,
# ) -> typing.Tuple[types.TReturnValue, _TReturnSchema]:
#     """
#     Generate column based on OpenAPI schema property.

#     Args:
#         schema: The schema for the column.
#         model_schema: The schema of the model.
#         schemas: Used to resolve any $ref.
#         required: Whether the object property is required.
#         logical_name: The logical name in the specification for the schema.

#     Returns:
#         The logical name, the SQLAlchemy column based on the schema and the
#         specification to store for the column.

#     """
#     artifacts = property_.get(
#         schemas=schemas,
#         model_schema=model_schema,
#         property_name=logical_name,
#         schema=schema,
#         required=required,
#     )
