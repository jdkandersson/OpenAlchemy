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


@pytest.mark.parametrize(
    "name, value",
    [
        ("x-backref", True),
        ("x-primary-key", "True"),
        ("x-autoincrement", "True"),
        ("x-index", "True"),
        ("x-unique", "True"),
        ("x-foreign-key", True),
        ("x-foreign-key", "no column"),
        ("x-foreign-key-column", True),
        ("x-tablename", True),
        ("x-de-$ref", True),
    ],
    ids=[
        "x-backref",
        "x-primary-key",
        "x-autoincrement",
        "x-index",
        "x-unique",
        "x-foreign-key invalid type",
        "x-foreign-key invalid format",
        "x-foreign-key-column",
        "x-tablename",
        "x-de-$ref",
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
        ("x-primary-key", True),
        ("x-autoincrement", True),
        ("x-index", True),
        ("x-unique", True),
        ("x-foreign-key", "table 1.column 1"),
        ("x-foreign-key-column", "column 1"),
        ("x-tablename", "table 1"),
        ("x-de-$ref", "Table1"),
    ],
    ids=[
        "x-backref",
        "x-primary-key",
        "x-autoincrement",
        "x-index",
        "x-unique",
        "x-foreign-key",
        "x-foreign-key-column",
        "x-tablename",
        "x-de-$ref",
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
