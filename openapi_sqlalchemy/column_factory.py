"""Generate columns based on openapi schema property."""

import typing

import sqlalchemy


def column_factory(*, schema: typing.Dict[str, typing.Any]) -> sqlalchemy.Column:
    """
    Generate column based on openapi schema property.

    Args:
        schema: The schema for the column.
        required: Whether the object property is required.

    Returns:
        The SQLAlchemy column based on the schema.

    """
    if "type" not in schema:
        raise TypeError("Every property requires a type.")

    # Keep track of column arguments
    type_: typing.Optional[sqlalchemy.sql.type_api.TypeEngine] = None
    args: typing.Tuple[typing.Any, ...] = ()
    kwargs: typing.Dict[str, typing.Any] = {}

    if schema["type"] == "number":
        type_ = sqlalchemy.Float

    if type_ is None:
        raise NotImplementedError(f"{schema['type']} has not been implemented")

    return sqlalchemy.Column(type_, *args, **kwargs)
