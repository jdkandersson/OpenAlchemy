"""Tests for ext_prop."""

import functools

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.helper
def test_miss():
    """
    GIVEN empty source
    WHEN get is called with the source
    THEN None is returned.
    """
    assert helpers.ext_prop.get(source={}, name="missing") is None


@pytest.mark.helper
def test_miss_default():
    """
    GIVEN empty source and default value
    WHEN get is called with the source and default value
    THEN default value is returned.
    """
    default = "value 1"

    value = helpers.ext_prop.get(source={}, name="missing", default=default)

    assert value == default


@pytest.mark.parametrize(
    "name, value",
    [
        ("x-backref", True),
        ("x-uselist", "True"),
        ("x-secondary", True),
        ("x-primary-key", "True"),
        ("x-autoincrement", "True"),
        ("x-index", "True"),
        ("x-unique", "True"),
        ("x-foreign-key", True),
        ("x-foreign-key", "no column"),
        ("x-foreign-key-column", True),
        ("x-tablename", True),
        ("x-tablename", None),
        ("x-de-$ref", True),
        ("x-dict-ignore", "True"),
        ("x-generated", "True"),
    ],
    ids=[
        "x-backref",
        "x-uselist",
        "x-secondary",
        "x-primary-key",
        "x-autoincrement",
        "x-index",
        "x-unique",
        "x-foreign-key invalid type",
        "x-foreign-key invalid format",
        "x-foreign-key-column",
        "x-tablename",
        "x-tablename None",
        "x-de-$ref",
        "x-dict-ignore",
        "x-generated",
    ],
)
@pytest.mark.helper
def test_invalid(name, value):
    """
    GIVEN property and invalid value
    WHEN get is called with a source made of the property and value
    THEN MalformedExtensionPropertyError is raised.
    """
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.ext_prop.get(source=source, name=name)


@pytest.mark.parametrize(
    "name, value",
    [
        ("x-backref", "table 1"),
        ("x-uselist", True),
        ("x-secondary", "association"),
        ("x-primary-key", True),
        ("x-autoincrement", True),
        ("x-index", True),
        ("x-unique", True),
        ("x-foreign-key", "table 1.column 1"),
        ("x-foreign-key-column", "column 1"),
        ("x-tablename", "table 1"),
        ("x-de-$ref", "Table1"),
        ("x-dict-ignore", True),
        ("x-generated", True),
    ],
    ids=[
        "x-backref",
        "x-uselist",
        "x-secondary",
        "x-primary-key",
        "x-autoincrement",
        "x-index",
        "x-unique",
        "x-foreign-key",
        "x-foreign-key-column",
        "x-tablename",
        "x-de-$ref",
        "x-dict-ignore",
        "x-generated",
    ],
)
@pytest.mark.helper
def test_valid(name, value):
    """
    GIVEN property and valid value
    WHEN get is called with a source made of the property and value
    THEN the value is returned.
    """
    source = {name: value}

    returned_value = helpers.ext_prop.get(source=source, name=name)

    assert returned_value == value


@pytest.mark.helper
def test_pop():
    """
    GIVEN property and valid value
    WHEN geterty is called with the name, value and pop set
    THEN the key is removed from the dictionary.
    """
    name = "x-dict-ignore"
    value = True
    source = {name: value}

    returned_value = helpers.ext_prop.get(source=source, name=name, pop=True)

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
    WHEN get with x-composite-unique and the value
    THEN MalformedExtensionPropertyError is raised.
    """
    name = "x-composite-unique"
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.ext_prop.get(source=source, name=name)


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
    WHEN get with x-composite-unique and the value
    THEN the value is returned.
    """
    name = "x-composite-unique"
    source = {name: value}

    returned_value = helpers.ext_prop.get(source=source, name=name)

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
    WHEN get with x-composite-index and the value
    THEN MalformedExtensionPropertyError is raised.
    """
    name = "x-composite-index"
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.ext_prop.get(source=source, name=name)


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
    WHEN get is called with x-composite-index and the value
    THEN the value is returned.
    """
    name = "x-composite-index"
    source = {name: value}

    returned_value = helpers.ext_prop.get(source=source, name=name)

    assert returned_value == value


@pytest.mark.parametrize(
    "value",
    [
        "RefSchema",
        {"ref_schema": "RefSchema"},
        {"ref_schema": {"x-de-$ref": "RefSchema"}},
        {"ref_schema": {"type": "object"}},
        {"ref_schema": {"type": "object", "x-de-$ref": True}},
        {"ref_schema": {"type": "object", "x-de-$ref": None}},
        {"ref_schema": {"type": True, "x-de-$ref": "RefSchem"}},
        {"ref_schema": {"type": None, "x-de-$ref": "RefSchem"}},
        {"ref_schema": {"type": "array"}},
        {"ref_schema": {"type": "array", "items": {}}},
    ],
    ids=[
        "not object",
        "object not of object",
        "object object object type type missing",
        "object object object type x-de-$ref missing",
        "object object object type x-de-$ref wrong type",
        "object object object type x-de-$ref null",
        "object object object type type wrong type",
        "object object object type type null",
        "object object array type  items missing",
        "object object array type  items empty",
    ],
)
@pytest.mark.helper
def test_relationship_backrefs_invalid(value):
    """
    GIVEN value for x-backrefs with an invalid format
    WHEN get is called with x-backrefs and the value
    THEN MalformedExtensionPropertyError is raised.
    """
    name = "x-backrefs"
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.ext_prop.get(source=source, name=name)


@pytest.mark.parametrize(
    "value",
    [
        {},
        {"ref_schema": {"type": "object", "x-de-$ref": "RefSchema"}},
        {
            "ref_schema": {
                "type": "array",
                "items": {"type": "object", "x-de-$ref": "RefSchema"},
            }
        },
        {
            "ref_schema1": {"type": "object", "x-de-$ref": "RefSchema1"},
            "ref_schema2": {"type": "object", "x-de-$ref": "RefSchema2"},
        },
    ],
    ids=["empty", "single object type", "single array type", "multiple"],
)
@pytest.mark.helper
def test_relationship_backrefs_valid(value):
    """
    GIVEN value for x-backrefs with a valid format
    WHEN get is called with x-backrefs and the value
    THEN value is returned.
    """
    name = "x-backrefs"
    source = {name: value}

    return_value = helpers.ext_prop.get(source=source, name=name)

    assert return_value == value


@pytest.mark.parametrize(
    "value",
    [
        "value",
        ["value"],
        {1: "value"},
        {1: "value 1", 2: "value 2"},
        {"key 1": "value 1", 2: "value 2"},
    ],
    ids=[
        "simple",
        "array",
        "object not string key",
        "object multiple key none string",
        "object multiple key some string",
    ],
)
@pytest.mark.helper
def test_kwargs_invalid(value):
    """
    GIVEN value for x-kwargs that has an invalid format
    WHEN get_kwargs is called with the value
    THEN MalformedExtensionPropertyError is raised.
    """
    name = "x-kwargs"
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.ext_prop.get_kwargs(source=source)


@pytest.mark.parametrize(
    "value",
    [
        {"key": "value"},
        {"key1": "value 1", "key2": "value 2"},
        {"key": ["value"]},
        {"key": {"sub_key": "value"}},
        {"key": {1: "value"}},
    ],
    ids=[
        "simple value",
        "simple value multiple keys",
        "array value",
        "object simple string key value",
        "object simple integer key value",
    ],
)
@pytest.mark.helper
def test_kwargs_valid(value):
    """
    GIVEN value for x-kwargs that has a valid format
    WHEN get_kwargs is called with the value
    THEN the value is returned.
    """
    name = "x-kwargs"
    source = {name: value}

    returned_value = helpers.ext_prop.get_kwargs(source=source)

    assert returned_value == value


@pytest.mark.helper
def test_kwargs_valid_name():
    """
    GIVEN value for kwargs that has a valid format and a property name
    WHEN get_kwargs is called with the value and the name
    THEN the value is returned.
    """
    name = "x-foreign-key-kwargs"
    value = {"key": "value"}
    source = {name: value}

    returned_value = helpers.ext_prop.get_kwargs(source=source, name=name)

    assert returned_value == value


@pytest.mark.helper
def test_kwargs_valid_missing():
    """
    GIVEN empty value
    WHEN get_kwargs is called with the value
    THEN None is returned.
    """
    source = {}

    returned_value = helpers.ext_prop.get_kwargs(source=source)

    assert returned_value is None


@pytest.mark.parametrize(
    "reserved, value, raises",
    [
        (set(), {}, False),
        (set(), {"key 1": "value 1"}, False),
        (set(), {"key 1": "value 1", "key 2": "value 2"}, False),
        ({"key 1"}, {}, False),
        ({"key 1"}, {"key 1": "value 1"}, True),
        ({"key 1"}, {"key 2": "value 2"}, False),
        ({"key 1"}, {"key 1": "value 1", "key 2": "value 2"}, True),
        ({"key 1"}, {"key 2": "value 2", "key 3": "value 3"}, False),
        ({"key 1", "key 2"}, {}, False),
        ({"key 1", "key 2"}, {"key 1": "value 1"}, True),
        ({"key 1", "key 2"}, {"key 2": "value 2"}, True),
        ({"key 1", "key 2"}, {"key 3": "value 3"}, False),
    ],
    ids=[
        "empty reserved    empty keys",
        "empty reserved    single key",
        "empty reserved    multiple keys",
        "single reserved   empty keys",
        "single reserved   single key    hit",
        "single reserved   single key    miss",
        "single reserved   multiple keys hit",
        "single reserved   multiple keys miss",
        "multiple reserved empty keys",
        "multiple reserved single key    first hit",
        "multiple reserved single key    second hit",
        "multiple reserved single key    miss",
    ],
)
@pytest.mark.helper
def test_kwargs_reserved(reserved, value, raises):
    """
    GIVEN value for x-kwargs, set of reserved keys and whether to raise
    WHEN get_kwargs is called with the value and reserved keys
    THEN MalformedExtensionPropertyError is raised if it is expected to raise.
    """
    name = "x-kwargs"
    source = {name: value}

    test_func = functools.partial(
        helpers.ext_prop.get_kwargs, source=source, reserved=reserved
    )
    if raises:
        with pytest.raises(exceptions.MalformedExtensionPropertyError):
            test_func()
    else:
        returned_value = test_func()

        assert returned_value == value
