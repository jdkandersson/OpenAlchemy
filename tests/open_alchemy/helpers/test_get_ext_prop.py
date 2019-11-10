"""Tests for get_ext_prop."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.helper
def test_miss():
    """
    GIVEN empty source
    WHEN get_ext_prop is called with the source
    THEN None is returned.
    """
    assert helpers.get_ext_prop(source={}, name="missing") is None


@pytest.mark.helper
def test_miss_default():
    """
    GIVEN empty source and default value
    WHEN get_ext_prop is called with the source and default value
    THEN default value is returned.
    """
    default = "value 1"

    value = helpers.get_ext_prop(source={}, name="missing", default=default)

    assert value == default


@pytest.mark.parametrize(
    "name, value",
    [
        ("x-backref", True),
        ("x-uselist", "True"),
        ("x-primary-key", "True"),
        ("x-autoincrement", "True"),
        ("x-index", "True"),
        ("x-unique", "True"),
        ("x-foreign-key", True),
        ("x-foreign-key", "no column"),
        ("x-foreign-key-column", True),
        ("x-tablename", True),
        ("x-de-$ref", True),
        ("x-dict-ignore", "True"),
    ],
    ids=[
        "x-backref",
        "x-uselist",
        "x-primary-key",
        "x-autoincrement",
        "x-index",
        "x-unique",
        "x-foreign-key invalid type",
        "x-foreign-key invalid format",
        "x-foreign-key-column",
        "x-tablename",
        "x-de-$ref",
        "x-dict-ignore",
    ],
)
@pytest.mark.helper
def test_invalid(name, value):
    """
    GIVEN property and invalid value
    WHEN get_ext_prop is called with a source made of the property and value
    THEN MalformedExtensionPropertyError is raised.
    """
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.get_ext_prop(source=source, name=name)


@pytest.mark.parametrize(
    "name, value",
    [
        ("x-backref", "table 1"),
        ("x-uselist", True),
        ("x-primary-key", True),
        ("x-autoincrement", True),
        ("x-index", True),
        ("x-unique", True),
        ("x-foreign-key", "table 1.column 1"),
        ("x-foreign-key-column", "column 1"),
        ("x-tablename", "table 1"),
        ("x-de-$ref", "Table1"),
        ("x-dict-ignore", True),
    ],
    ids=[
        "x-backref",
        "x-uselist",
        "x-primary-key",
        "x-autoincrement",
        "x-index",
        "x-unique",
        "x-foreign-key",
        "x-foreign-key-column",
        "x-tablename",
        "x-de-$ref",
        "x-dict-ignore",
    ],
)
@pytest.mark.helper
def test_valid(name, value):
    """
    GIVEN property and valid value
    WHEN get_ext_prop is called with a source made of the property and value
    THEN the value is returned.
    """
    source = {name: value}

    returned_value = helpers.get_ext_prop(source=source, name=name)

    assert returned_value == value


def test_pop():
    """
    GIVEN property and valid value
    WHEN get_ext_property is called with the name, value and pop set
    THEN the key is removed from the dictionary.
    """
    name = "x-dict-ignore"
    value = True
    source = {name: value}

    returned_value = helpers.get_ext_prop(source=source, name=name, pop=True)

    assert returned_value == value
    assert source == {}


@pytest.mark.parametrize(
    "value",
    ["column 1", [], [[]], [None], [1], {}, {"name": 1}],
    ids=[
        "not object not array",
        "empty list",
        "empty list of list",
        "list of null",
        "list of not string",
        "object columns missing",
        "object name not string",
    ],
)
@pytest.mark.helper
def test_unique_constraint_invalid(value):
    """
    GIVEN value for x-composite-unique that has an invalid format
    WHEN get_ext_prop with x-composite-unique and the value
    THEN MalformedExtensionPropertyError is raised.
    """
    name = "x-composite-unique"
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.get_ext_prop(source=source, name=name)


@pytest.mark.parametrize(
    "value",
    [
        ["column 1"],
        [["column 1"]],
        {"columns": ["column 1"]},
        {"columns": ["column 1"], "name": "name 1"},
        [{"columns": ["column 1"]}],
    ],
    ids=[
        "list of string",
        "list of list of string",
        "object with columns",
        "object with columns and name",
        "list of object with columns",
    ],
)
@pytest.mark.helper
def test_unique_constraint_valid(value):
    """
    GIVEN value for x-composite-unique that has a valid format
    WHEN get_ext_prop with x-composite-unique and the value
    THEN the value is returned.
    """
    name = "x-composite-unique"
    source = {name: value}

    returned_value = helpers.get_ext_prop(source=source, name=name)

    assert returned_value == value


@pytest.mark.parametrize(
    "value",
    [
        "column 1",
        [],
        [[]],
        [None],
        [1],
        {},
        {"name": 1, "expressions": ["column 1"]},
        {"expressions": ["column 1"], "unique": "true"},
    ],
    ids=[
        "not object not array",
        "empty list",
        "empty list of list",
        "list of null",
        "list of not string",
        "object expressions missing",
        "object name not string",
        "object unique not boolean",
    ],
)
@pytest.mark.helper
def test_composite_index_invalid(value):
    """
    GIVEN value for x-composite-index that has an invalid format
    WHEN get_ext_prop with x-composite-index and the value
    THEN MalformedExtensionPropertyError is raised.
    """
    name = "x-composite-index"
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.get_ext_prop(source=source, name=name)


@pytest.mark.parametrize(
    "value",
    [
        ["column 1"],
        [["column 1"]],
        {"expressions": ["column 1"]},
        {"name": "name 1", "expressions": ["column 1"]},
        {"expressions": ["column 1"], "unique": True},
        [{"expressions": ["column 1"]}],
    ],
    ids=[
        "list of string",
        "list of list of string",
        "object",
        "object name",
        "object unique",
        "list of object",
    ],
)
@pytest.mark.helper
def test_composite_index_valid(value):
    """
    GIVEN value for x-composite-index that has a valid format
    WHEN get_ext_prop with x-composite-index and the value
    THEN the value is returned.
    """
    name = "x-composite-index"
    source = {name: value}

    returned_value = helpers.get_ext_prop(source=source, name=name)

    assert returned_value == value
