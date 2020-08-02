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


def calculate_property_name_x_to_one(
    *, property_name: str, foreign_key_column_name: str
) -> str:
    """
    Calculate the foreign key property name.

    Args:
        property_name: The name of the property that defines the relationship.
        foreign_key_column_name: The name of the foreign key column.

    Returns:
        The name of the foreign key property.

    """
    return f"{property_name}_{foreign_key_column_name}"
