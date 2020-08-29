"""Tests for table args factories."""

import functools

import pytest

from open_alchemy import exceptions
from open_alchemy.table_args import factory


@pytest.mark.parametrize(
    "spec, expected_name",
    [
        (["column 1"], "ColumnList"),
        ([["column 1"]], "ColumnListList"),
        ({"columns": ["column 1"]}, "Unique"),
        ({"columns": ["column 1"], "name": "name 1"}, "Unique"),
        ([{"columns": ["column 1"]}], "UniqueList"),
        ({"expressions": ["column 1"], "unique": True}, "Index"),
        ({"name": "name 1", "expressions": ["column 1"]}, "Index"),
        ({"name": "name 1", "expressions": ["column 1"], "unique": True}, "Index"),
        ([{"name": "name 1", "expressions": ["column 1"]}], "IndexList"),
    ],
    ids=[
        "ColumnList",
        "ColumnListList",
        "Unique no name",
        "Unique",
        "UniqueList",
        "Index no name",
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
    name = factory._spec_to_schema_name(spec=spec)  # pylint: disable=protected-access

    assert name == expected_name


@pytest.mark.parametrize(
    "schema_names, spec, raises",
    [
        ([], ["column 1"], True),
        (["ColumnListList"], ["column 1"], True),
        (["ColumnList"], ["column 1"], False),
        (["ColumnListList", "Unique"], ["column 1"], True),
        (["ColumnList", "Unique"], ["column 1"], False),
        (["Unique", "ColumnList"], ["column 1"], False),
    ],
    ids=[
        "empty schemas,    -,             raises",
        "single schemas,   spec diff,     raises",
        "single schemas,   spec match,    not raises",
        "multiple schemas, spec not in,   raises",
        "multiple schemas, spec in,       not raises",
        "multiple schemas, other spec in, not raises",
    ],
)
@pytest.mark.table_args
def test_spec_to_name_schemas(schema_names, spec, raises):
    """
    GIVEN list of schema names, spec and whether a raise is expected
    WHEN _spec_to_schema_name is called with the spec and schemas
    THEN SchemaNotFoundError is raised is a raise is expected.
    """
    test_func = functools.partial(
        factory._spec_to_schema_name,  # pylint: disable=protected-access
        spec=spec,
        schema_names=schema_names,
    )

    if raises:
        with pytest.raises(exceptions.SchemaNotFoundError):
            test_func()
    else:
        test_func()


@pytest.mark.parametrize(
    "spec, expected_spec",
    [
        (["column 1"], [{"columns": ["column 1"]}]),
        ([["column 1"]], [{"columns": ["column 1"]}]),
        (
            [["column 1"], ["column 2"]],
            [{"columns": ["column 1"]}, {"columns": ["column 2"]}],
        ),
        ({"columns": ["column 1"]}, [{"columns": ["column 1"]}]),
        ([{"columns": ["column 1"]}], [{"columns": ["column 1"]}]),
    ],
    ids=[
        "column list",
        "column list of list single",
        "column list of list multiple",
        "unique constraint",
        "list of unique constraint",
    ],
)
@pytest.mark.table_args
def test_map_unique(spec, expected_spec):
    """
    GIVEN specification and expected specification
    WHEN map_unique is called with the specification
    THEN the expected specification is returned which is a valid UniqueList.
    """
    returned_spec = factory.map_unique(spec=spec)  # pylint: disable=protected-access

    assert returned_spec == expected_spec
    assert (
        factory._spec_to_schema_name(  # pylint: disable=protected-access
            spec=returned_spec
        )
        == "UniqueList"
    )


@pytest.mark.parametrize(
    "spec, expected_columns",
    [
        pytest.param(
            ["column 1"],
            ["column 1"],
            id="column list single",
        ),
        pytest.param(
            ["column 1", "column 2"],
            ["column 1", "column 2"],
            id="column list multiple",
        ),
        pytest.param(
            [["column 1"]],
            ["column 1"],
            id="column list of list single",
        ),
        pytest.param(
            [["column 1"], ["column 2"]],
            ["column 1", "column 2"],
            id="column list of list multiple",
        ),
        pytest.param(
            {"columns": ["column 1"]},
            ["column 1"],
            id="unique constraint single",
        ),
        pytest.param(
            {"columns": ["column 1", "column 2"]},
            ["column 1", "column 2"],
            id="unique constraint multiple",
        ),
        pytest.param(
            [{"columns": ["column 1"]}],
            ["column 1"],
            id="list of unique constraint single",
        ),
        pytest.param(
            [{"columns": ["column 1"]}, {"columns": ["column 2"]}],
            ["column 1", "column 2"],
            id="list of unique constraint multiple",
        ),
    ],
)
@pytest.mark.table_args
def test_iter_unique_columns(spec, expected_columns):
    """
    GIVEN specification and expected columns
    WHEN iter_unique_columns is called with the specification
    THEN an iterator with all columns is returned.
    """
    returned_columns = factory.iter_unique_columns(spec=spec)

    assert list(returned_columns) == expected_columns


@pytest.mark.parametrize(
    "spec, expected_spec",
    [
        (["column 1"], [{"expressions": ["column 1"]}]),
        ([["column 1"]], [{"expressions": ["column 1"]}]),
        (
            [["column 1"], ["column 2"]],
            [{"expressions": ["column 1"]}, {"expressions": ["column 2"]}],
        ),
        ({"expressions": ["column 1"]}, [{"expressions": ["column 1"]}]),
        ([{"expressions": ["column 1"]}], [{"expressions": ["column 1"]}]),
    ],
    ids=[
        "column list",
        "column list of list single",
        "column list of list multiple",
        "composite index",
        "list of composite index",
    ],
)
@pytest.mark.table_args
def test_map_index(spec, expected_spec):
    """
    GIVEN specification and expected specification
    WHEN map_index is called with the specification
    THEN the expected specification is returned which is a valid IndexList.
    """
    returned_spec = factory.map_index(spec=spec)  # pylint: disable=protected-access

    assert returned_spec == expected_spec
    assert (
        factory._spec_to_schema_name(  # pylint: disable=protected-access
            spec=returned_spec
        )
        == "IndexList"
    )


@pytest.mark.parametrize(
    "spec, expected_expressions",
    [
        pytest.param(
            ["column 1"],
            ["column 1"],
            id="column list single",
        ),
        pytest.param(
            ["column 1", "column 2"],
            ["column 1", "column 2"],
            id="column list multiple",
        ),
        pytest.param(
            [["column 1"]],
            ["column 1"],
            id="column list of list single",
        ),
        pytest.param(
            [["column 1"], ["column 2"]],
            ["column 1", "column 2"],
            id="column list of list multiple",
        ),
        pytest.param(
            {"expressions": ["column 1"]},
            ["column 1"],
            id="unique constraint single",
        ),
        pytest.param(
            {"expressions": ["column 1", "column 2"]},
            ["column 1", "column 2"],
            id="unique constraint multiple",
        ),
        pytest.param(
            [{"expressions": ["column 1"]}],
            ["column 1"],
            id="list of unique constraint single",
        ),
        pytest.param(
            [{"expressions": ["column 1"]}, {"expressions": ["column 2"]}],
            ["column 1", "column 2"],
            id="list of unique constraint multiple",
        ),
    ],
)
@pytest.mark.table_args
def test_iter_index_expressions(spec, expected_expressions):
    """
    GIVEN specification and expected expressions
    WHEN iter_index_expressions is called with the specification
    THEN an iterator with all expressions is returned.
    """
    returned_expressions = factory.iter_index_expressions(spec=spec)

    assert list(returned_expressions) == expected_expressions


@pytest.mark.parametrize(
    "spec, expected_name, expected_columns",
    [
        ({"columns": ["column 1"]}, None, ["column 1"]),
        ({"name": "name 1", "columns": ["column 1"]}, "name 1", ["column 1"]),
        ({"columns": ["column 1", "column 2"]}, None, ["column 1", "column 2"]),
    ],
    ids=["single", "single name", "multiple"],
)
@pytest.mark.table_args
def test_construct_unique(spec, expected_name, expected_columns):
    """
    GIVEN spec, expected name and columns
    WHEN _construct_unique is called
    THEN a unique constraint with the expected name and columns is returned.
    """
    assert (
        factory._spec_to_schema_name(spec=spec)  # pylint: disable=protected-access
        == "Unique"
    )

    unique = factory._construct_unique(spec=spec)  # pylint: disable=protected-access

    assert unique.name == expected_name
    assert (
        unique._pending_colargs == expected_columns  # pylint: disable=protected-access
    )


@pytest.mark.parametrize(
    "spec, expected_name, expected_expressions, expected_unique",
    [
        pytest.param(
            {"expressions": ["column 1"]}, None, ["column 1"], False, id="single"
        ),
        pytest.param(
            {"name": "name 1", "expressions": ["column 1"]},
            "name 1",
            ["column 1"],
            False,
            id="single name",
        ),
        pytest.param(
            {"expressions": ["column 1"], "unique": True},
            None,
            ["column 1"],
            True,
            id="single unique True",
        ),
        pytest.param(
            {"expressions": ["column 1"], "unique": False},
            None,
            ["column 1"],
            False,
            id="single unique False",
        ),
        pytest.param(
            {"expressions": ["column 1", "column 2"]},
            None,
            ["column 1", "column 2"],
            False,
            id="multiple",
        ),
    ],
)
@pytest.mark.table_args
def test_construct_index(spec, expected_name, expected_expressions, expected_unique):
    """
    GIVEN spec, expected name, expressions and unique
    WHEN _construct_index is called
    THEN a index with the expected name, expressions and unique is returned.
    """
    assert (
        factory._spec_to_schema_name(spec=spec)  # pylint: disable=protected-access
        == "Index"
    )

    index = factory._construct_index(spec=spec)  # pylint: disable=protected-access

    assert index.name == expected_name
    assert index.expressions == expected_expressions
    assert index.unique == expected_unique


@pytest.mark.table_args
def test_unique_factory():
    """
    GIVEN specification
    WHEN unique_factory is called with the specification
    THEN UniqueConstraints are returned.
    """
    spec = [["column 1"], ["column 2"]]

    unique_1, unique_2 = factory.unique_factory(spec=spec)

    assert unique_1._pending_colargs == ["column 1"]  # pylint: disable=protected-access
    assert unique_2._pending_colargs == ["column 2"]  # pylint: disable=protected-access


@pytest.mark.table_args
def test_index_factory():
    """
    GIVEN specification
    WHEN index_factory is called with the specification
    THEN UniqueConstraints are returned.
    """
    spec = [["column 1"], ["column 2"]]

    index_1, index_2 = factory.index_factory(spec=spec)

    assert index_1.expressions == ["column 1"]
    assert index_2.expressions == ["column 2"]
