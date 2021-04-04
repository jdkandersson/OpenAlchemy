"""Tests for table_args functions."""

import pytest
from sqlalchemy import schema as sa_schema

from open_alchemy import table_args
from open_alchemy import types


@pytest.mark.parametrize(
    "schema, expected_args",
    [
        pytest.param({}, ({},), id="empty"),
        pytest.param(
            {"x-composite-unique": ["column 1"]},
            (sa_schema.UniqueConstraint, {}),
            id="x-composite-unique",
        ),
        pytest.param(
            {"x-composite-index": ["column 1"]},
            (sa_schema.Index, {}),
            id="x-composite-index",
        ),
        pytest.param(
            {"x-schema-name": "schema 1"},
            ({"schema": "schema 1"},),
            id="x-schema-name",
        ),
        pytest.param(
            {
                "x-composite-unique": ["column 1"],
                "x-composite-index": ["column 2"],
                "x-schema-name": "schema 1",
            },
            (sa_schema.UniqueConstraint, sa_schema.Index, {"schema": "schema 1"}),
            id="all",
        ),
    ],
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
    for returned_arg, expected_arg in zip(returned_args[:-1], expected_args[:-1]):
        assert isinstance(returned_arg, expected_arg)
    assert returned_args[-1] == expected_args[-1]


@pytest.mark.parametrize(
    "schema, expected_kwargs",
    [
        pytest.param({}, {}, id="empty"),
        pytest.param({"key": "value"}, {}, id="different key"),
        pytest.param(
            {types.ExtensionProperties.SCHEMA_NAME: "schema 1"},
            {"schema": "schema 1"},
            id="schema name",
        ),
    ],
)
@pytest.mark.table_args
def test_calculate_kwargs(schema, expected_kwargs):
    """
    GIVEN schema
    WHEN _calculate_kwargs is called with the schema
    THEN the expected kwargs are returned.
    """
    kwargs = table_args._calculate_kwargs(  # pylint: disable=protected-access
        schema=schema
    )

    assert kwargs == expected_kwargs
