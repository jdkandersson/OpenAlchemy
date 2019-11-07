"""Create table args such as UniqueConstraints and Index."""

import typing

from open_alchemy import types


def _handle_column_list(spec: typing.List[str]) -> types.UniqueConstraint:
    """
    Convert ColumnList specification to UniqueConstrain.

    Args:
        spec: The specification to convert.

    Returns:
        The UniqueConstraint.

    """
    return {"columns": spec}


_UNIQUE_MAPPING: typing.Dict[str, typing.Callable[..., types.UniqueConstraintList]] = {
    "ColumnList": lambda spec: [_handle_column_list(spec=spec)],
    "ColumnListList": lambda spec: list(map(_handle_column_list, spec)),
    "UniqueConstraint": lambda spec: [spec],
    "uniqueConstraintList": lambda spec: spec,
}


# def _handle_unique(*, spec: types.AnyUniqueConstraint) -> types.UniqueConstraintList:
#     """
#     Convert any unique constraint to UniqueConstraintList.

#     Args:
#         spec: The specification to convert.

#     Returns:
#         The UniqueConstraintList.

#     """
