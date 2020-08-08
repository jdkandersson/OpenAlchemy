"""Helpers for properties."""

from .... import types as oa_types
from ... import helpers
from .. import types


def check_properties_values(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """
    Check the values of the properties.

    Args:
        schema: The schema to check.
        schemas: All defined schemas used to resolve any $ref.

    Returns:
    The result if the properties values are not valid with a reason or None.

    """
    properties_values = helpers.iterate.properties_values(
        schema=schema, schemas=schemas
    )
    not_dict_value = next(
        filter(lambda arg: not isinstance(arg, dict), properties_values), None
    )
    if not_dict_value is not None:
        return types.Result(False, "value of properties must be a dictionary")
    return None
