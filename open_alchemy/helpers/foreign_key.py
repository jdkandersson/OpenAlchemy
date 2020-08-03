"""Helpers for foreign keys."""

from .. import types
from . import peek
from . import relationship


def calculate_column_name(
    *, type_: relationship.Type, property_schema: types.Schema, schemas: types.Schemas
) -> str:
    """
    Calculate the column name based on the relationship property schema.

    Assume the property is a x-to-one or one-to-many relationship.
    Assume the relationship property schema is valid.

    Args:
        type_: The type of relationship the schema defines.
        property_schema: The schema of the relationship property.
        schemas: All defined schemas used to resolve any $ref.

    Returns:
        The name of the foreign key column.

    """
    assert type_ != relationship.Type.MANY_TO_MANY

    if type_ == relationship.Type.ONE_TO_MANY:
        items_schema = peek.items(schema=property_schema, schemas=schemas)
        assert items_schema is not None
        property_schema = items_schema

    x_foreign_key_column = peek.foreign_key_column(
        schema=property_schema, schemas=schemas
    )
    return x_foreign_key_column if x_foreign_key_column is not None else "id"


def calculate_prop_name_x_to_one(
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


def calculate_prop_name_one_to_many(
    *, tablename: str, property_name: str, foreign_key_column_name: str
) -> str:
    """
    Calculate the foreign key property name.

    Args:
        tablename: The name of the table targeted by the foreign key.
        property_name: The name of the property that defines the relationship.
        foreign_key_column_name: The name of the foreign key column.

    Returns:
        The name of the foreign key property.

    """
    x_to_one_property_name = calculate_prop_name_x_to_one(
        property_name=property_name, foreign_key_column_name=foreign_key_column_name
    )
    return f"{tablename}_{x_to_one_property_name}"


# def calculate_prop_name(
#     *,
#     type_: relationship.Type,
#     foreign_key_targeted_schema: types.Schema,
#     schemas: types.Schemas,
# ) -> str:
#     """"""


def calculate_foreign_key(*, tablename: str, foreign_key_column_name: str) -> str:
    """
    Calculate the foreign key property name.

    Args:
        tablename: The name of the table targeted by the foreign key.
        foreign_key_column_name: The name of the foreign key column.

    Returns:
        The name of the foreign key property.

    """
    return f"{tablename}.{foreign_key_column_name}"
