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


def check_properties_items(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """
    Check the items of the properties.

    Args:
        schema: The schema to check.
        schemas: All defined schemas used to resolve any $ref.

    Returns:
    The result if the properties items are not valid with a reason or None.

    """
    # Check names are string and values are dictionaries
    properties_items = helpers.iterate.properties_items(schema=schema, schemas=schemas)

    def check_property(args) -> types.OptResult:
        """Check key and value of property."""
        key, value = args
        if not isinstance(key, str):
            return types.Result(False, f"property names must be strings, {key} is not")
        if not isinstance(value, dict):
            return types.Result(False, f"{key} :: property values must be dictionaries")
        return None

    # Check for any results
    properties_items_results = map(check_property, properties_items)
    first_result = next(filter(None, properties_items_results), None)
    if first_result is not None:
        return first_result

    return None
