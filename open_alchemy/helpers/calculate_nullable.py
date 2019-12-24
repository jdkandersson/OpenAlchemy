"""Calculate whether a column is nullable."""

import typing


def calculate_nullable(
    *, nullable: typing.Optional[bool], required: typing.Optional[bool]
) -> bool:
    """
    Calculate the value of the nullable field.

    The following is the truth table for the nullable property.
    required  | schema nullable | returned nullable
    --------------------------------------------------------
    None      | not given       | True
    None      | False           | False
    None      | True            | True
    False     | not given       | True
    False     | False           | False
    False     | True            | True
    True      | not given       | False
    True      | False           | False
    True      | True            | True

    To summarize, if nullable is the schema the value for it is used. Otherwise True
    is returned unless required is True.

    Args:
        nullable: Whether the property is nullable.
        required: Whether the property is required.

    Returns:
        The nullable value for the column.

    """
    if nullable is None:
        if required:
            return False
        return True
    if nullable:
        return True
    return False
