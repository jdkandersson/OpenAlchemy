"""Helpers for foreign keys."""

import typing


def calculate_column_name(*, x_foreign_key_column: typing.Optional[str]) -> str:
    """
    Calculate the column name based on the value of x-foreign-key-column.

    Args:
        x_foreign_key_column: The value of x-foreign-key column.

    Returns:
        The name of the foreign key column.

    """
    return x_foreign_key_column if x_foreign_key_column is not None else "id"
