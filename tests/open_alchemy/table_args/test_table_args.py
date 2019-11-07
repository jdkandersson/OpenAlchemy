"""Tests for table_args functions."""

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


@pytest.mark.table_args
def test_spec_to_schema_name_not_found():
    """
    GIVEN spec that does not match a schema
    WHEN _spec_to_schema_name is called with the spec
    THEN SchemaNotFoundError is raised.
    """
    with pytest.raises(exceptions.SchemaNotFoundError):
        table_args._spec_to_schema_name(spec="")  # pylint: disable=protected-access
