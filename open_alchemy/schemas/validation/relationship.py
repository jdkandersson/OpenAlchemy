"""Define validation rules for relationship."""

import typing

# from ... import types


class Result(typing.NamedTuple):
    """Result of checking a schema."""

    # Whether the schema is valid
    valid: bool
    # If not valid, the reason why it isn't
    reason: typing.Optional[str]


# def check(schemas: types.Schemas, schema: types.Schema) -> Result:
#     """
#     Check whether a property schema is a valid relationship schema.

#     Args:
#         schemas: All the defined schemas used to resolve any $ref.
#         schema: The schema to check.

#     Returns:
#         Whether the schema is a valid relationship.

#     """
