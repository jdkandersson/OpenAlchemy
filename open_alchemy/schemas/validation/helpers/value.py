"""Validate the full schema (property, source and referenced)."""

import typing

from .... import types as oa_types
from ....helpers import peek


def check_matches(
    *,
    func: peek.PeekValue,
    reference_schema: oa_types.Schema,
    check_schema: oa_types.Schema,
    schemas: oa_types.Schemas,
) -> typing.Optional[str]:
    """
    Check that the value matches in two schemas.

    Args:
        func: Used to retrieve the value.
        reference_schema: The schema to check against.
        check_schema: The schema to check
        schemas: All defined schemas, used to resolve any $ref.

    Returns:
        An invalid result with reason if the values don't match otherwise None.

    """
    expected_value = peek.prefer_local(
        get_value=func, schema=reference_schema, schemas=schemas
    )
    if expected_value is None:
        expected_value_str = "not to be defined"
    else:
        expected_value_str = f'"{expected_value}"'

    actual_value = peek.prefer_local(
        get_value=func, schema=check_schema, schemas=schemas
    )
    if actual_value is None:
        actual_value_str = "not defined"
    else:
        actual_value_str = f'"{actual_value}"'

    if expected_value != actual_value:
        return f"expected {expected_value_str}, actual is {actual_value_str}"

    return None
