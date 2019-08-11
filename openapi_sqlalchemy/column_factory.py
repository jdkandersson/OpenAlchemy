"""Generate columns based on openapi schema property."""

import typing

import sqlalchemy


def column_factory(
    *, schema: typing.Dict[str, typing.Any], required: bool = False
) -> sqlalchemy.Column:
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

    if required:
        kwargs["nullable"] = False

    if schema.get("x-primary-key"):
        kwargs["primary_key"] = True

    if schema.get("type") == "integer":
        type_ = _handle_integer(schema=schema)

    if schema.get("type") == "number":
        type_ = sqlalchemy.Float

    if type_ is None:
        raise NotImplementedError(f"{schema['type']} has not been implemented")

    return sqlalchemy.Column(type_, *args, **kwargs)


def _handle_integer(
    *, schema: typing.Dict[str, typing.Any]
) -> typing.Union[sqlalchemy.Integer, sqlalchemy.BigInteger]:
    """
    Determine the type of integer to use for the schema.

    Args:
        schema: The schema for the integer column.

    Returns:
        Integer or BigInteger depending on the format.

    """
    if schema.get("format", "int32") == "int32":
        return sqlalchemy.Integer
    if schema.get("format") == "int64":
        return sqlalchemy.BigInteger
    raise NotImplementedError(
        f"{schema.get('format')} format for integer is not supported."
    )
