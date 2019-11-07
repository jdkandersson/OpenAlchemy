"""Generate columns based on OpenAPI schema property."""

import re
import typing

import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types

from . import column
from . import object_ref

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


def column_factory(
    *,
    spec: types.Schema,
    schemas: types.Schemas,
    required: typing.Optional[bool] = None,
    logical_name: str,
) -> typing.Tuple[typing.List[typing.Tuple[str, sqlalchemy.Column]], types.Schema]:
    """
    Generate column based on OpenAPI schema property.

    Args:
        spec: The schema for the column.
        schemas: Used to resolve any $ref.
        required: Whether the object property is required.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name, the SQLAlchemy column based on the schema and the
        specification to store for the column.

    """
    # Checking for the type
    type_ = helpers.peek_type(schema=spec, schemas=schemas)

    # CHandling columns
    if type_ != "object":
        spec = helpers.prepare_schema(schema=spec, schemas=schemas)
        return (
            column.handle_column(
                logical_name=logical_name, spec=spec, required=required
            ),
            spec,
        )

    # Handling objects
    return object_ref.handle_object(
        spec=spec, schemas=schemas, required=required, logical_name=logical_name
    )
