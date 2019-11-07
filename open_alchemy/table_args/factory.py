"""Create table args such as UniqueConstraints and Index."""

import typing

from sqlalchemy import schema


def _handle_column_list(
    *, spec: typing.List[str]
) -> typing.List[schema.UniqueConstraint]:
    """
    Convert ColumnList specification to UniqueConstraint.

    Args:
        spec: The specification to convert.

    Returns:
        The UniqueConstraint.

    """
    return [schema.UniqueConstraint(*spec)]
