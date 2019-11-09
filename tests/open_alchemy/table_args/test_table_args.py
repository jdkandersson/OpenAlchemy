"""Tests for table_args functions."""

import pytest
from sqlalchemy import schema as sa_schema

from open_alchemy import table_args


@pytest.mark.parametrize(
    "schema, expected_args",
    [
        ({}, tuple()),
        ({"x-composite-unique": ["column 1"]}, (sa_schema.UniqueConstraint,)),
        ({"x-composite-index": ["column 1"]}, (sa_schema.Index,)),
        (
            {"x-composite-unique": ["column 1"], "x-composite-index": ["column 2"]},
            (sa_schema.UniqueConstraint, sa_schema.Index),
        ),
    ],
    ids=["empty", "x-composite-unique", "x-composite-index", "all"],
)
@pytest.mark.table_args
def test_construct(schema, expected_args):
    """
    GIVEN schema and expected constructed table arg types
    WHEN construct is called with the schema
    THEN a tuple with the expected table args is returned.
    """
    returned_args = table_args.construct(schema=schema)

    assert len(returned_args) == len(expected_args)
    for returned_arg, expected_arg in zip(returned_args, expected_args):
        assert isinstance(returned_arg, expected_arg)
