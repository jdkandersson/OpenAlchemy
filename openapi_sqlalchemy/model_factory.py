"""Generate model from openapi schema."""

import itertools
import typing

from . import column_factory
from . import exceptions
from . import helpers
from . import types


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
    schema_spec: types.SchemaSpec = schemas.get(name, {})
    # De-referencing schema
    schema_spec = helpers.resolve_ref(
        schema=types.Schema(name, schema_spec), schemas=schemas
    ).spec
    # Checking for tablename key
    if "x-tablename" not in schema_spec:
        raise exceptions.MalformedSchemaError(
            f'"x-tablename" is a required schema property for {name}.'
        )
    # Checking for object type
    if schema_spec.get("type") != "object":
        raise exceptions.FeatureNotImplementedError(
            f"{schema_spec.get('type')} is not supported in {name}."
        )
    if not schema_spec.get("properties"):
        raise exceptions.MalformedSchemaError(
            f"At least 1 property is required for {name}."
        )

    # Assembling model
    return type(
        name,
        (base,),
        {
            "__tablename__": schema_spec.get("x-tablename"),
            **dict(
                itertools.chain.from_iterable(
                    # pylint: disable=unexpected-keyword-arg
                    column_factory.column_factory(
                        spec=value,
                        schemas=schemas,
                        logical_name=key,
                        required=key in schema_spec.get("required", [])
                        if "required" in schema_spec
                        else None,
                    )
                    for key, value in schema_spec.get("properties", []).items()
                )
            ),
        },
    )
