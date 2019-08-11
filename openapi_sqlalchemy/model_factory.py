"""Generate model from openapi schema."""

import typing


def model_factory(*, name: str, schemas: typing.Dict[str, typing.Any]) -> None:
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
        raise KeyError(f"{name} not found in schemas")
    schema = schemas[name]
    # Checking for tablename key
    if "x-tablename" not in schema:
        raise TypeError('"x-tablename" is a required schema property.')
    # Checking for object type
    if schema.get("type") != "object":
        raise NotImplementedError(f"{schema.get('type')} is not supported.")
    if not schema.get("properties"):
        raise TypeError("At least 1 property is required.")
