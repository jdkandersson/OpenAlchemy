"""Tests for table_args functions."""

import pytest

from open_alchemy import table_args


@pytest.mark.parametrize(
    "schema, expected_length",
    [
        ({}, 0),
        ({"x-unique-constraint": ["column 1"]}, 1),
        ({"x-composite-index": ["column 1"]}, 1),
        ({"x-unique-constraint": ["column 1"], "x-composite-index": ["column 2"]}, 2),
    ],
    ids=["empty", "x-unique-constraint", "x-composite-index", "all"],
)
@pytest.mark.table_args
def test_construct(schema, expected_length):
    """
    GIVEN schema and expected length
    WHEN construct is called with the schema
    THEN a tuple with the expected length is returned.
    """
    returned_args = table_args.construct(schema=schema)

    assert len(returned_args) == expected_length
