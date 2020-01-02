"""Calculate whether a column is nullable."""

import typing


def calculate_nullable(
    *, nullable: typing.Optional[bool], generated: bool, required: typing.Optional[bool]
) -> bool:
    """
    Calculate the value of the nullable field.

    The following is the truth table for the nullable property.
    +------------+-----------+-----------------+-------------------+
    | required   | generated | schema nullable | returned nullable |
    +============+===========+=================+===================+
    | None/False | False     | not given       | True              |
    +------------+-----------+-----------------+-------------------+
    | None/False | True      | not given       | False             |
    +------------+-----------+-----------------+-------------------+
    | True       | X         | not given       | False             |
    +------------+-----------+-----------------+-------------------+
    | X          | X         | False           | False             |
    +------------+-----------+-----------------+-------------------+
    | X          | X         | True            | True              |
    +------------+-----------+-----------------+-------------------+

    To summarize, if nullable is the schema the value for it is used. Otherwise True
    is returned unless required is True or generated is True.

    Args:
        nullable: Whether the property is nullable.
        generated: Whether the column gets generated in some form (eg. auto increment,
            default value).
        required: Whether the property is required.

    Returns:
        The nullable value for the column.

    """
    if nullable is None:
        if required:
            return False
        if generated:
            return False
        return True
    if nullable:
        return True
    return False
