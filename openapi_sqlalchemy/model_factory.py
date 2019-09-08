"""Generate model from openapi schema."""

import itertools
import typing

from . import column_factory
from . import exceptions


def model_factory(
    *,
    name: str,
    base: typing.Type,
    schemas: typing.Dict[str, typing.Dict[str, typing.Any]],
) -> typing.Type:
    """
    Convert openapi schema to SQLAlchemy model.

    Args:
        name: The name of the schema.
        base: The SQLAlchemy declarative base.
        schemas: The openapi schemas.

    Returns:
        The model as a class.

    """
    # Input validation
    # Checking that name is in schemas
    if name not in schemas:
        raise exceptions.SchemaNotFoundError(f"{name} not found in schemas")
    schema: typing.Dict[str, typing.Any] = schemas.get(name, {})
    # Checking for tablename key
    if "x-tablename" not in schema:
        raise exceptions.MalformedSchemaError(
            '"x-tablename" is a required schema property.'
        )
    # Checking for object type
    if schema.get("type") != "object":
        raise exceptions.FeatureNotImplementedError(
            f"{schema.get('type')} is not supported."
        )
    if not schema.get("properties"):
        raise exceptions.MalformedSchemaError("At least 1 property is required.")

    # Assembling model
    return type(
        name,
        (base,),
        {
            "__tablename__": schema.get("x-tablename"),
            **dict(
                itertools.chain.from_iterable(
                    # pylint: disable=unexpected-keyword-arg
                    column_factory.column_factory(
                        spec=value,
                        schemas=schemas,
                        logical_name=key,
                        required=key in schema.get("required", [])
                        if "required" in schema
                        else None,
                    )
                    for key, value in schema.get("properties", []).items()
                )
            ),
        },
    )
