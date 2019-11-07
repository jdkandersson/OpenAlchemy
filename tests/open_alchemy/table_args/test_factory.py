"""Tests for table args factories."""
# pylint: disable=protected-access

# import pytest

# from open_alchemy.table_args import factory


# @pytest.mark.parametrize(
#     "spec",
#     [["column 1"], ["column 1", "column 2"]],
#     ids=["single", "multiple"],
# )
# @pytest.mark.table_args
# def test_handle_column_list(spec):
#     """
#     GIVEN list of columns
#     WHEN _handle_column_list is called
#     THEN list of unique constraints is returned.
#     """
#     unique_list = factory._handle_column_list(spec=spec)

#     assert unique_list == [{"columns": spec}]


# @pytest.mark.parametrize(
#     "spec",
#     [[["column 1"]], [["column 1"], ["column 2"]]],
#     ids=["single", "multiple"],
# )
# @pytest.mark.table_args
# def test_handle_column_list_list(spec):
#     """
#     GIVEN list of list of columns
#     WHEN _handle_column_list_list is called
#     THEN indexes with columns are returned.
#     """
#     indexes = factory._handle_column_list_list(spec=spec)

#     mapped_indexes = list(map(lambda index: index._pending_colargs))
