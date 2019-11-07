"""Tests for table_args functions."""

import functools

import pytest

from open_alchemy import exceptions
from open_alchemy import table_args


@pytest.mark.parametrize(
    "spec, expected_name",
    [
        (["column 1"], "ColumnList"),
        ([["column 1"]], "ColumnListList"),
        ({"columns": ["column 1"]}, "UniqueConstraint"),
        ({"columns": ["column 1"], "name": "name 1"}, "UniqueConstraint"),
        ([{"columns": ["column 1"]}], "UniqueConstraintList"),
        ({"name": "name 1", "expressions": ["column 1"]}, "Index"),
        ({"name": "name 1", "expressions": ["column 1"], "unique": True}, "Index"),
        ([{"name": "name 1", "expressions": ["column 1"]}], "IndexList"),
    ],
    ids=[
        "ColumnList",
        "ColumnListList",
        "UniqueConstraint no name",
        "UniqueConstraint",
        "UniqueConstraintList",
        "Index no unique",
        "Index",
        "IndexList",
    ],
)
@pytest.mark.table_args
def test_spec_to_schema_name(spec, expected_name):
    """
    GIVEN spec and expected name
    WHEN _spec_to_schema_name is called with the spec
    THEN the expected name is returned
    """
    name = table_args._spec_to_schema_name(  # pylint: disable=protected-access
        spec=spec
    )

    assert name == expected_name


@pytest.mark.parametrize(
    "schema_names, spec, raises",
    [
        ([], ["column 1"], True),
        (["ColumnListList"], ["column 1"], True),
        (["ColumnList"], ["column 1"], False),
        (["ColumnListList", "UniqueConstraint"], ["column 1"], True),
        (["ColumnList", "UniqueConstraint"], ["column 1"], False),
        (["UniqueConstraint", "ColumnList"], ["column 1"], False),
    ],
    ids=[
        "empty schemas,   -,              raises",
        "single schemas,   spec diff,     raises",
        "single schemas,   spec match,    not raises",
        "multiple schemas, spec not in,   raises",
        "multiple schemas, spec in,       not raises",
        "multiple schemas, other spec in, not raises",
    ],
)
@pytest.mark.table_args
def test_spec_to_schemas(schema_names, spec, raises):
    """
    GIVEN list of schema names, spec and whether a raise is expected
    WHEN _spec_to_schema_name is called with the spec and schemas
    THEN SchemaNotFoundError is raised is a raise is expected.
    """
    test_func = functools.partial(
        table_args._spec_to_schema_name,  # pylint: disable=protected-access
        spec=spec,
        schema_names=schema_names,
    )

    if raises:
        with pytest.raises(exceptions.SchemaNotFoundError):
            test_func()
    else:
        test_func()
