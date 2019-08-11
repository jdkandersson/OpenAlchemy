"""Map an openapi schema to SQLAlchemy models."""

import typing


def _model_factory(*, name: str, schemas: typing.Dict[str, typing.Any]) -> None:
    """
    Convert openapi schema to SQLAlchemy model.

    Args:
        name: The name of the schema.
        base: The SQLAlchemy declarative base.
        schemas: The openapi schemas.

    Returns:
        The model as a class.

    """
    # Checking that name is in schemas
    if name not in schemas:
        raise KeyError(f"{name} not found in schemas")
