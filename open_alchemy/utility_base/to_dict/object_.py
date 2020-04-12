"""Dictionary conversion for object."""

import typing

from ... import exceptions


def _convert_relationship(*, value: typing.Any) -> typing.Dict[str, typing.Any]:
    """
    Convert object relationship property to a dictionary.

    Raises InvalidModelInstanceError if the value does not have a to_dict function.
    Raises InvalidModelInstanceError if the value has a to_dict function that expects
        arguments.

    Args:
        value: The value to convert.

    Returns:
        The object as a dictionary.

    """
    try:
        return value.to_dict()
    except AttributeError:
        raise exceptions.InvalidModelInstanceError(
            f"The object property instance does not have a to_dict " "implementation."
        )
    except TypeError:
        raise exceptions.InvalidModelInstanceError(
            f"The object property instance to_dict implementation is "
            "expecting arguments."
        )
