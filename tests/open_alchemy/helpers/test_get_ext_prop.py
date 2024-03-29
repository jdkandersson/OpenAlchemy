"""Tests for ext_prop."""

import functools

import pytest

from open_alchemy import exceptions
from open_alchemy import types
from open_alchemy.helpers import ext_prop


@pytest.mark.helper
def test_miss():
    """
    GIVEN empty source
    WHEN get is called with the source
    THEN None is returned.
    """
    assert ext_prop.get(source={}, name="missing") is None


@pytest.mark.helper
def test_miss_default():
    """
    GIVEN empty source and default value
    WHEN get is called with the source and default value
    THEN default value is returned.
    """
    default = "value 1"

    value = ext_prop.get(source={}, name="missing", default=default)

    assert value == default


@pytest.mark.parametrize(
    "name, value",
    [
        pytest.param("x-backref", True, id="x-backref"),
        pytest.param("x-uselist", "True", id="x-uselist"),
        pytest.param("x-secondary", True, id="x-secondary"),
        pytest.param("x-primary-key", "True", id="x-primary-key"),
        pytest.param("x-autoincrement", "True", id="x-autoincrement"),
        pytest.param("x-index", "True", id="x-index"),
        pytest.param("x-unique", "True", id="x-unique"),
        pytest.param("x-json", "True", id="x-json"),
        pytest.param("x-foreign-key", True, id="x-foreign-key invalid type"),
        pytest.param("x-foreign-key", "no column", id="x-foreign-key invalid format"),
        pytest.param("x-foreign-key-column", True, id="x-foreign-key-column"),
        pytest.param("x-server-default", True, id="x-server-default"),
        pytest.param("x-tablename", True, id="x-tablename"),
        pytest.param("x-tablename", None, id="x-tablename None"),
        pytest.param("x-schema-name", True, id="x-schema-name"),
        pytest.param("x-de-$ref", True, id="x-de-$ref"),
        pytest.param("x-dict-ignore", "True", id="x-dict-ignore"),
        pytest.param("x-generated", "True", id="x-generated"),
        pytest.param("x-inherits", 1, id="x-inherits"),
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
        ext_prop.get(source=source, name=name)


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in types.KeyPrefixes],
)
@pytest.mark.parametrize(
    "name, value",
    [
        pytest.param(
            "backref",
            "table 1",
            id="backref",
        ),
        pytest.param(
            "uselist",
            True,
            id="uselist",
        ),
        pytest.param(
            "secondary",
            "association",
            id="secondary",
        ),
        pytest.param(
            "primary-key",
            True,
            id="primary-key",
        ),
        pytest.param(
            "autoincrement",
            True,
            id="autoincrement",
        ),
        pytest.param(
            "index",
            True,
            id="index",
        ),
        pytest.param(
            "unique",
            True,
            id="unique",
        ),
        pytest.param(
            "json",
            True,
            id="json",
        ),
        pytest.param(
            "foreign-key",
            "table 1.column 1",
            id="foreign-key",
        ),
        pytest.param(
            "foreign-key-column",
            "column 1",
            id="foreign-key-column",
        ),
        pytest.param(
            "server-default",
            "value 1",
            id="server-default",
        ),
        pytest.param(
            "tablename",
            "table 1",
            id="tablename",
        ),
        pytest.param(
            "schema-name",
            "schema 1",
            id="schema-name",
        ),
        pytest.param(
            "de-$ref",
            "Table1",
            id="de-$ref",
        ),
        pytest.param(
            "dict-ignore",
            True,
            id="dict-ignore",
        ),
        pytest.param(
            "generated",
            True,
            id="generated",
        ),
        pytest.param(
            "inherits",
            True,
            id="inherits bool",
        ),
        pytest.param(
            "inherits",
            "Parent",
            id="inherits string",
        ),
    ],
)
@pytest.mark.helper
def test_valid(prefix, name, value):
    """
    GIVEN prefix, property and valid value
    WHEN get is called with a source made of the property and value
    THEN the value is returned.
    """
    source = {f"{prefix}{name}": value}

    returned_value = ext_prop.get(
        source=source, name=f"{types.KeyPrefixes.SHORT}{name}"
    )

    assert returned_value == value


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in types.KeyPrefixes],
)
@pytest.mark.helper
def test_pop(prefix):
    """
    GIVEN prefix, property and valid value
    WHEN get is called with the name, value and pop set
    THEN the key is removed from the dictionary.
    """
    name = "dict-ignore"
    value = True
    source = {f"{prefix}{name}": value}

    returned_value = ext_prop.get(
        source=source, name=f"{types.KeyPrefixes.SHORT}{name}", pop=True
    )

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
        ext_prop.get(source=source, name=name)


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in types.KeyPrefixes],
)
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
def test_unique_constraint_valid(prefix, value):
    """
    GIVEN prefix and value for x-composite-unique that has a valid format
    WHEN get with x-composite-unique and the value
    THEN the value is returned.
    """
    name = "composite-unique"
    source = {f"{prefix}{name}": value}

    returned_value = ext_prop.get(
        source=source, name=f"{types.KeyPrefixes.SHORT}{name}"
    )

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
        ext_prop.get(source=source, name=name)


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in types.KeyPrefixes],
)
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
def test_composite_index_valid(prefix, value):
    """
    GIVEN prefix and value for x-composite-index that has a valid format
    WHEN get is called with x-composite-index and the value
    THEN the value is returned.
    """
    name = "composite-index"
    source = {f"{prefix}{name}": value}

    returned_value = ext_prop.get(
        source=source, name=f"{types.KeyPrefixes.SHORT}{name}"
    )

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
        ext_prop.get(source=source, name=name)


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in types.KeyPrefixes],
)
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
def test_relationship_backrefs_valid(prefix, value):
    """
    GIVEN prefix and value for x-backrefs with a valid format
    WHEN get is called with x-backrefs and the value
    THEN value is returned.
    """
    name = "backrefs"
    source = {f"{prefix}{name}": value}

    return_value = ext_prop.get(source=source, name=f"{types.KeyPrefixes.SHORT}{name}")

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
        ext_prop.get_kwargs(source=source)


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in types.KeyPrefixes],
)
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
def test_kwargs_valid(prefix, value):
    """
    GIVEN prefix and value for x-kwargs that has a valid format
    WHEN get_kwargs is called with the value
    THEN the value is returned.
    """
    name = "kwargs"
    source = {f"{prefix}{name}": value}

    returned_value = ext_prop.get_kwargs(source=source)

    assert returned_value == value


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in types.KeyPrefixes],
)
@pytest.mark.helper
def test_kwargs_valid_name(prefix):
    """
    GIVEN prefix and value for kwargs that has a valid format and a property name
    WHEN get_kwargs is called with the value and the name
    THEN the value is returned.
    """
    name = "foreign-key-kwargs"
    value = {"key": "value"}
    source = {f"{prefix}{name}": value}

    returned_value = ext_prop.get_kwargs(
        source=source, name=f"{types.KeyPrefixes.SHORT}{name}"
    )

    assert returned_value == value


@pytest.mark.helper
def test_kwargs_valid_missing():
    """
    GIVEN empty value
    WHEN get_kwargs is called with the value
    THEN None is returned.
    """
    source = {}

    returned_value = ext_prop.get_kwargs(source=source)

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

    test_func = functools.partial(ext_prop.get_kwargs, source=source, reserved=reserved)
    if raises:
        with pytest.raises(exceptions.MalformedExtensionPropertyError):
            test_func()
    else:
        returned_value = test_func()

        assert returned_value == value


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(None, id="None"),
        pytest.param(1, id="not string"),
        pytest.param("", id="empty string"),
        pytest.param([], id="list empty"),
        pytest.param([None], id="list contains None"),
    ],
)
@pytest.mark.helper
def test_mixins_invalid(value):
    """
    GIVEN value for x-mixins that has an invalid format
    WHEN get with x-mixins and the value
    THEN MalformedExtensionPropertyError is raised.
    """
    name = "x-mixins"
    source = {name: value}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        ext_prop.get(source=source, name=name)


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in types.KeyPrefixes],
)
@pytest.mark.parametrize(
    "value",
    [
        pytest.param("mixin 1", id="string"),
        pytest.param(["mixin 1"], id="lst single"),
        pytest.param(["mixin 1", "mixin 1"], id="lst multiple"),
    ],
)
@pytest.mark.helper
def test_mixins_valid(prefix, value):
    """
    GIVEN prefix and value for x-mixins that has a valid format
    WHEN get with x-mixins and the value
    THEN the value is returned.
    """
    name = "mixins"
    source = {f"{prefix}{name}": value}

    returned_value = ext_prop.get(
        source=source, name=f"{types.KeyPrefixes.SHORT}{name}"
    )

    assert returned_value == value
