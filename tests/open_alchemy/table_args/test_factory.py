"""Tests for table args factories."""

# import pytest

# from open_alchemy.table_args import factory


# @pytest.mark.table_args
# def test_handle_column_list():
#     """
#     GIVEN list of columns
#     WHEN _handle_column_list is called
#     THEN list of unique constraints is returned.
#     """
#     spec = ["column 1"]

#     unique_list = factory._handle_column_list(  # pylint: disable=protected-access
#         spec=spec
#     )

#     assert unique_list == [{"columns": ["column 1"]}]


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
