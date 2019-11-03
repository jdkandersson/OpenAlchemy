"""Generate model from OpenAPI schema."""

import itertools
import typing

from . import column_factory
from . import exceptions
from . import helpers
from . import types


def model_factory(
    *, name: str, base: typing.Type, schemas: types.Schemas
) -> typing.Type:
    """
    Convert OpenAPI schema to SQLAlchemy model.

    Args:
        name: The name of the schema.
        base: The SQLAlchemy declarative base.
        schemas: The OpenAPI schemas.

    Returns:
        The model as a class.

    """
    # Input validation
    # Checking that name is in schemas
    if name not in schemas:
        raise exceptions.SchemaNotFoundError(f"{name} not found in schemas")
    schema: types.Schema = schemas.get(name, {})
    # De-referencing schema
    schema = helpers.prepare_schema(schema=schema, schemas=schemas)
    # Checking for tablename key
    if "x-tablename" not in schema:
        raise exceptions.MalformedSchemaError(
            f'"x-tablename" is a required schema property for {name}.'
        )
    # Checking for object type
    if schema.get("type") != "object":
        raise exceptions.FeatureNotImplementedError(
            f"{schema.get('type')} is not supported in {name}."
        )
    if not schema.get("properties"):
        raise exceptions.MalformedSchemaError(
            f"At least 1 property is required for {name}."
        )

    # Assembling model
    return type(
        name,
        (base,),
        {
            "__tablename__": helpers.get_ext_prop(source=schema, name="x-tablename"),
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
