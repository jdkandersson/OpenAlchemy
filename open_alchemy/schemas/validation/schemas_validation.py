"""Check the schemas are valid."""

import typing

from . import types


def check(*, schemas: typing.Any) -> types.Result:
    """
    Check that the schemas are valid.

    Algorithm:
    1. check that it is a dictionary,
    2. check that every key is a string and
    3. check that every value is a dictionary.

    Args:
        schemas: The schemas to check.

    Returns:
        Whether the schemas are valid and the reason if they are not.

    """
    if not isinstance(schemas, dict):
        return types.Result(False, "schemas must be a dictionary")

    # Check keys are strings
    first_key_not_string = next(
        filter(lambda key: not isinstance(key, str), schemas.keys()),
        None,
    )
    if first_key_not_string is not None:
        return types.Result(
            False, f"schemas keys must be strings, {first_key_not_string} is not"
        )

    # Check values are dictionaries
    first_item_not_dict_value = next(
        filter(lambda args: not isinstance(args[1], dict), schemas.items()), None
    )
    if first_item_not_dict_value is not None:
        key, _ = first_item_not_dict_value
        return types.Result(False, f"the value of {key} must be a dictionary")

    return types.Result(True, None)
