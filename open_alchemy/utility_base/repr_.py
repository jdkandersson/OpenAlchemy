"""Calculate the repr for the model."""

import typing

from open_alchemy import types


def calculate(*, instance: typing.Any, properties: types.Schema) -> str:
    """
    Calculate the repr for the model.

    The repr is the string that would be needed to create an equivalent instance of the
    model.

    Args:
        instance: The model instance to calculate the repr for.
        properties: The properties of the model instance.

    Returns:
        The string that would be needed to create an equivalent instance of the model.

    """
    # Calculate the name
    name = type(instance).__name__

    # Retrieve property values
    prop_repr_gen = (
        (prop, repr(getattr(instance, prop, None))) for prop in properties.keys()
    )
    prop_repr_str_gen = (f"{name}={value}" for name, value in prop_repr_gen)
    prop_repr_str = ", ".join(prop_repr_str_gen)

    # Calculate repr
    return f"open_alchemy.models.{name}({prop_repr_str})"
