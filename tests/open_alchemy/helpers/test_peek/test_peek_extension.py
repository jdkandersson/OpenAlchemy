"""Tests for peek helpers."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.helper
def test_autoincrement_wrong_type():
    """
    GIVEN schema with autoincrement defined as a string
    WHEN autoincrement is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-autoincrement": "True"}
    schema = {"x-open-alchemy-autoincrement": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.autoincrement(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_autoincrement",
    [
        ({}, None),
        ({"x-autoincrement": True}, True),
        ({"x-autoincrement": False}, False),
        ({"x-open-alchemy-autoincrement": True}, True),
        ({"x-open-alchemy-autoincrement": False}, False),
    ],
    ids=["missing", "true", "false", "true", "false"],
)
@pytest.mark.helper
def test_autoincrement(schema, expected_autoincrement):
    """
    GIVEN schema and expected autoincrement
    WHEN autoincrement is called with the schema
    THEN the expected autoincrement is returned.
    """
    returned_autoincrement = helpers.peek.autoincrement(schema=schema, schemas={})

    assert returned_autoincrement == expected_autoincrement


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-index": "True"}),
        ({"x-open-alchemy-index": "True"}),
    ],
)
@pytest.mark.helper
def test_index_wrong_type(schema):
    """
    GIVEN schema with index defined as a string
    WHEN index is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.index(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_index",
    [
        ({}, None),
        ({"x-index": True}, True),
        ({"x-index": False}, False),
        ({"x-open-alchemy-index": True}, True),
        ({"x-open-alchemy-index": False}, False),
    ],
    ids=["missing", "true", "false", "true", "false"],
)
@pytest.mark.helper
def test_index(schema, expected_index):
    """
    GIVEN schema and expected index
    WHEN index is called with the schema
    THEN the expected index is returned.
    """
    returned_index = helpers.peek.index(schema=schema, schemas={})

    assert returned_index == expected_index


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-unique": "True"}),
        ({"x-open-alchemy-unique": "True"}),
    ],
)
@pytest.mark.helper
def test_unique_wrong_type(schema):
    """
    GIVEN schema with unique defined as a string
    WHEN unique is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.unique(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_unique",
    [
        ({}, None),
        ({"x-unique": True}, True),
        ({"x-unique": False}, False),
        ({"x-open-alchemy-unique": True}, True),
        ({"x-open-alchemy-unique": False}, False),
    ],
    ids=["missing", "true", "false", "true", "false"],
)
@pytest.mark.helper
def test_unique(schema, expected_unique):
    """
    GIVEN schema and expected unique
    WHEN unique is called with the schema
    THEN the expected unique is returned.
    """
    returned_unique = helpers.peek.unique(schema=schema, schemas={})

    assert returned_unique == expected_unique


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-primary-key": "True"}),
        ({"x-open-alchemy-primary-key": "True"}),
    ],
)
@pytest.mark.helper
def test_primary_key_wrong_type(schema):
    """
    GIVEN schema with primary key defined as a string
    WHEN primary_key is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.primary_key(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_primary_key",
    [
        pytest.param({}, None, id="missing"),
        pytest.param({"x-primary-key": False}, False, id="False"),
        pytest.param({"x-primary-key": True}, True, id="True"),
        pytest.param(
            {"x-open-alchemyprimary-key": False},
            False,
            id="False",
            marks=pytest.mark.xfail,
        ),
        pytest.param(
            {"x-open-alchemyprimary-key": True},
            True,
            id="True",
            marks=pytest.mark.xfail,
        ),
    ],
)
@pytest.mark.helper
def test_primary_key(schema, expected_primary_key):
    """
    GIVEN schema and expected primary key
    WHEN primary_key is called with the schema
    THEN the expected primary key is returned.
    """
    returned_primary_key = helpers.peek.primary_key(schema=schema, schemas={})

    assert returned_primary_key == expected_primary_key


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-tablename": True}),
        pytest.param({"x-open-alchemy-tablename": True}, marks=pytest.mark.xfail),
    ],
)
@pytest.mark.helper
def test_tablename_wrong_type(schema):
    """
    GIVEN schema with tablename defined as a boolean
    WHEN tablename is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.tablename(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_tablename",
    [
        ({}, None),
        ({"x-tablename": "table 1"}, "table 1"),
        ({"x-open-alchemy-tablename": "table 1"}, "table 1"),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_tablename(schema, expected_tablename):
    """
    GIVEN schema and expected tablename
    WHEN tablename is called with the schema
    THEN the expected tablename is returned.
    """
    returned_tablename = helpers.peek.tablename(schema=schema, schemas={})

    assert returned_tablename == expected_tablename


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-inherits": 1}),
        ({"x-open-alchemy-inherits": 1}),
    ],
)
@pytest.mark.helper
def test_inherits_wrong_type(schema):
    """
    GIVEN schema with x-inherits defined as an integer
    WHEN inherits is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.inherits(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_inherits",
    [
        ({}, None),
        ({"x-inherits": "Parent1"}, "Parent1"),
        ({"x-inherits": True}, True),
        ({"x-open-alchemy-inherits": "Parent1"}, "Parent1"),
        ({"x-open-alchemy-inherits": True}, True),
    ],
    ids=[
        "missing",
        "defined string",
        "defined boolean",
        "defined string",
        "defined boolean",
    ],
)
@pytest.mark.helper
def test_inherits(schema, expected_inherits):
    """
    GIVEN schema and expected inherits
    WHEN inherits is called with the schema
    THEN the expected inherits is returned.
    """
    returned_inherits = helpers.peek.inherits(schema=schema, schemas={})

    assert returned_inherits == expected_inherits


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-json": 1}),
        ({"x-open-alchemy-json": 1}),
    ],
)
@pytest.mark.helper
def test_json_wrong_type(schema):
    """
    GIVEN schema with x-json defined as an integer
    WHEN json is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.json(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_json",
    [
        ({}, None),
        ({"x-json": True}, True),
        ({"x-open-alchemy-json": True}, True),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_json(schema, expected_json):
    """
    GIVEN schema and expected json
    WHEN json is called with the schema
    THEN the expected json is returned.
    """
    returned_json = helpers.peek.json(schema=schema, schemas={})

    assert returned_json == expected_json


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-backref": True}),
        ({"x-open-alchemy-backref": True}),
    ],
)
@pytest.mark.helper
def test_backref_wrong_type(schema):
    """
    GIVEN schema with backref defined as a boolean
    WHEN backref is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.backref(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_backref",
    [
        ({}, None),
        ({"x-backref": "table 1"}, "table 1"),
        ({"x-open-alchemy-backref": "table 1"}, "table 1"),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_backref(schema, expected_backref):
    """
    GIVEN schema and expected backref
    WHEN backref is called with the schema
    THEN the expected backref is returned.
    """
    returned_backref = helpers.peek.backref(schema=schema, schemas={})

    assert returned_backref == expected_backref


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-secondary": True}),
        ({"x-open-alchemy-secondary": True}),
    ],
)
@pytest.mark.helper
def test_secondary_wrong_type(schema):
    """
    GIVEN schema with secondary defined as a boolean
    WHEN secondary is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.secondary(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_secondary",
    [
        ({}, None),
        ({"x-secondary": "table 1"}, "table 1"),
        ({"x-open-alchemy-secondary": "table 1"}, "table 1"),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_secondary(schema, expected_secondary):
    """
    GIVEN schema and expected secondary
    WHEN secondary is called with the schema
    THEN the expected secondary is returned.
    """
    returned_secondary = helpers.peek.secondary(schema=schema, schemas={})

    assert returned_secondary == expected_secondary


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-uselist": "True"}),
        ({"x-open-alchemy-uselist": "True"}),
    ],
)
@pytest.mark.helper
def test_uselist_wrong_type(schema):
    """
    GIVEN schema with uselist defined as a boolean
    WHEN uselist is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.uselist(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_uselist",
    [
        ({}, None),
        ({"x-uselist": True}, True),
        ({"x-open-alchemy-uselist": True}, True),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_uselist(schema, expected_uselist):
    """
    GIVEN schema and expected uselist
    WHEN uselist is called with the schema
    THEN the expected uselist is returned.
    """
    returned_uselist = helpers.peek.uselist(schema=schema, schemas={})

    assert returned_uselist == expected_uselist


@pytest.mark.parametrize(
    "schema",
    [
        pytest.param({"x-kwargs": True}, id="not dict"),
        pytest.param({"x-kwargs": {1: True}}, id="single key not string"),
        pytest.param(
            {"x-kwargs": {1: True, "key": "value"}}, id="multiple key first not string"
        ),
        pytest.param(
            {"x-kwargs": {"key": "value", 1: True}}, id="multiple key second not string"
        ),
        pytest.param(
            {"x-kwargs": {1: True, 2: False}}, id="multiple key all not string"
        ),
        pytest.param({"x-open-alchemy-kwargs": True}, id="not dict"),
    ],
)
@pytest.mark.helper
def test_kwargs_wrong_type(schema):
    """
    GIVEN schema
    WHEN kwargs is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.kwargs(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_kwargs",
    [
        ({}, None),
        ({"x-kwargs": {"key": "value"}}, {"key": "value"}),
        ({"x-open-alchemy-kwargs": {"key": "value"}}, {"key": "value"}),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_kwargs(schema, expected_kwargs):
    """
    GIVEN schema and expected kwargs
    WHEN kwargs is called with the schema
    THEN the expected kwargs is returned.
    """
    returned_kwargs = helpers.peek.kwargs(schema=schema, schemas={})

    assert returned_kwargs == expected_kwargs


@pytest.mark.parametrize(
    "schema",
    [
        pytest.param({"x-foreign-key-kwargs": True}, id="not dict"),
        pytest.param({"x-foreign-key-kwargs": {1: True}}, id="single key not string"),
        pytest.param(
            {"x-foreign-key-kwargs": {1: True, "key": "value"}},
            id="multiple key first not string",
        ),
        pytest.param(
            {"x-foreign-key-kwargs": {"key": "value", 1: True}},
            id="multiple key second not string",
        ),
        pytest.param(
            {"x-foreign-key-kwargs": {1: True, 2: False}},
            id="multiple key all not string",
        ),
        pytest.param({"x-open-alchemy-foreign-key-kwargs": True}, id="not dict"),
    ],
)
@pytest.mark.helper
def test_foreign_key_kwargs_wrong_type(schema):
    """
    GIVEN schema
    WHEN foreign_key_kwargs is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.foreign_key_kwargs(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_foreign_key_kwargs",
    [
        ({}, None),
        ({"x-foreign-key-kwargs": {"key": "value"}}, {"key": "value"}),
        ({"x-open-alchemy-foreign-key-kwargs": {"key": "value"}}, {"key": "value"}),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_foreign_key_kwargs(schema, expected_foreign_key_kwargs):
    """
    GIVEN schema and expected foreign_key_kwargs
    WHEN foreign_key_kwargs is called with the schema
    THEN the expected foreign_key_kwargs is returned.
    """
    returned_foreign_key_kwargs = helpers.peek.foreign_key_kwargs(
        schema=schema, schemas={}
    )

    assert returned_foreign_key_kwargs == expected_foreign_key_kwargs


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-foreign-key": True}),
        ({"x-open-alchemy-foreign-key": True}),
    ],
)
@pytest.mark.helper
def test_foreign_key_wrong_type(schema):
    """
    GIVEN schema with foreign-key defined as a boolean
    WHEN foreign_key is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.foreign_key(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_foreign_key",
    [
        ({}, None),
        ({"x-foreign-key": "id"}, "id"),
        ({"x-open-alchemy-foreign-key": "id"}, "id"),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_foreign_key(schema, expected_foreign_key):
    """
    GIVEN schema and expected foreign-key
    WHEN foreign_key is called with the schema
    THEN the expected foreign_key is returned.
    """
    returned_foreign_key = helpers.peek.foreign_key(schema=schema, schemas={})

    assert returned_foreign_key == expected_foreign_key


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-foreign-key-column": True}),
        ({"x-open-alchemy-foreign-key-column": True}),
    ],
)
@pytest.mark.helper
def test_foreign_key_column_wrong_type(schema):
    """
    GIVEN schema with foreign-key-column defined as a boolean
    WHEN foreign_key_column is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.foreign_key_column(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_foreign_key_column",
    [
        ({}, None),
        ({"x-foreign-key-column": "id"}, "id"),
        ({"x-open-alchemy-foreign-key-column": "id"}, "id"),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_foreign_key_column(schema, expected_foreign_key_column):
    """
    GIVEN schema and expected foreign-key-column
    WHEN foreign_key_column is called with the schema
    THEN the expected foreign_key_column is returned.
    """
    returned_foreign_key_column = helpers.peek.foreign_key_column(
        schema=schema, schemas={}
    )

    assert returned_foreign_key_column == expected_foreign_key_column


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-composite-index": True}),
        ({"x-open-alchemy-composite-index": True}),
    ],
)
@pytest.mark.helper
def test_composite_index_wrong_type(schema):
    """
    GIVEN schema with composite-index defined as a boolean
    WHEN composite_index is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.peek.composite_index(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_composite_index",
    [
        ({}, None),
        ({"x-composite-index": ["id"]}, ["id"]),
        ({"x-open-alchemy-composite-index": ["id"]}, ["id"]),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_composite_index(schema, expected_composite_index):
    """
    GIVEN schema and expected composite-index
    WHEN composite_index is called with the schema
    THEN the expected composite_index is returned.
    """
    returned_composite_index = helpers.peek.composite_index(schema=schema, schemas={})

    assert returned_composite_index == expected_composite_index


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-composite-unique": True}),
        ({"x-open-alchemy-composite-unique": True}),
    ],
)
@pytest.mark.helper
def test_composite_unique_wrong_type(schema):
    """
    GIVEN schema with composite-unique defined as a boolean
    WHEN composite_unique is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.peek.composite_unique(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_composite_unique",
    [
        ({}, None),
        ({"x-composite-unique": ["id"]}, ["id"]),
        ({"x-open-alchemy-composite-unique": ["id"]}, ["id"]),
    ],
    ids=["missing", "defined", "defined"],
)
@pytest.mark.helper
def test_composite_unique(schema, expected_composite_unique):
    """
    GIVEN schema and expected composite-unique
    WHEN composite_unique is called with the schema
    THEN the expected composite_unique is returned.
    """
    returned_composite_unique = helpers.peek.composite_unique(schema=schema, schemas={})

    assert returned_composite_unique == expected_composite_unique


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-server-default": True}),
        ({"x-open-alchemy-server-default": True}),
    ],
)
@pytest.mark.helper
def test_server_default_wrong_type(schema):
    """
    GIVEN schema with server_default defined as a string
    WHEN server_default is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.server_default(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_server_default",
    [
        pytest.param({}, None, id="missing"),
        pytest.param({"x-server-default": "value 1"}, "value 1", id="defined"),
        pytest.param(
            {"x-open-alchemy-server-default": "value 1"}, "value 1", id="defined"
        ),
    ],
)
@pytest.mark.helper
def test_server_default(schema, expected_server_default):
    """
    GIVEN schema and expected server_default
    WHEN server_default is called with the schema
    THEN the expected server_default is returned.
    """
    returned_server_default = helpers.peek.server_default(schema=schema, schemas={})

    assert returned_server_default == expected_server_default


@pytest.mark.parametrize(
    "schema",
    [
        pytest.param({"x-mixins": "MissingDot"}, id="no dot"),
        pytest.param({"x-mixins": ".second"}, id="single dot leading not identifier"),
        pytest.param({"x-mixins": "first."}, id="single dot trailing not identifier"),
        pytest.param(
            {"x-mixins": ".second.third"}, id="multiple dot leading not identifier"
        ),
        pytest.param(
            {"x-mixins": "first..third"}, id="multiple dot middle not identifier"
        ),
        pytest.param(
            {"x-mixins": "first.second."}, id="multiple dot trailing not identifier"
        ),
        pytest.param({"x-mixins": ["first."]}, id="list single invalid"),
        pytest.param(
            {"x-mixins": ["first.", "first.second"]}, id="list multiple first invalid"
        ),
        pytest.param(
            {"x-mixins": ["first.second", ".second"]}, id="list multiple second invalid"
        ),
        pytest.param(
            {"x-mixins": ["first.", ".second"]}, id="list multiple all invalid"
        ),
        pytest.param({"x-open-alchemy-mixins": "MissingDot"}, id="no dot"),
    ],
)
@pytest.mark.helper
def test_mixins_invalid(schema):
    """
    GIVEN schema with an invalid mixins
    WHEN mixins is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.peek.mixins(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, schemas, expected_mixins",
    [
        pytest.param(
            {"x-mixins": "first.second"}, {}, ["first.second"], id="string single dot"
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-mixins": "first.second"}},
            ["first.second"],
            id="$ref string single dot",
        ),
        pytest.param(
            {"allOf": [{"x-mixins": "first.second"}]},
            {},
            ["first.second"],
            id="allOf string single dot",
        ),
        pytest.param(
            {"x-mixins": "first.second.third"},
            {},
            ["first.second.third"],
            id="string multiple dot",
        ),
        pytest.param(
            {"x-mixins": ["first.second"]}, {}, ["first.second"], id="list single"
        ),
        pytest.param(
            {"x-mixins": ["first.second1", "first.second2"]},
            {},
            ["first.second1", "first.second2"],
            id="list multiple",
        ),
        pytest.param(
            {"x-open-alchemy-mixins": "first.second"},
            {},
            ["first.second"],
            id="string single dot",
        ),
    ],
)
@pytest.mark.helper
def test_mixins(schema, schemas, expected_mixins):
    """
    GIVEN schema, schemas and expected mixins
    WHEN mixins is called with the schema and schemas
    THEN the expected mixins value is returned.
    """
    mixins = helpers.peek.mixins(schema=schema, schemas=schemas)

    assert mixins == expected_mixins


@pytest.mark.parametrize(
    "schema",
    [
        ({"x-dict-ignore": "True"}),
        pytest.param(
            {"x-open-alchemy-dict-ignore": "True"},
            marks=pytest.mark.xfail,
        ),
    ],
)
@pytest.mark.helper
def test_dict_ignore_wrong_type(schema):
    """
    GIVEN schema with dict_ignore defined as a string
    WHEN dict_ignore is called with the schema
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.dict_ignore(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_dict_ignore",
    [
        ({}, None),
        ({"x-dict-ignore": True}, True),
        ({"x-dict-ignore": False}, False),
        ({"x-open-alchemy-dict-ignore": True}, True),
        ({"x-open-alchemy-dict-ignore": False}, False),
    ],
    ids=["missing", "true", "false", "true", "false"],
)
@pytest.mark.helper
def test_dict_ignore(schema, expected_dict_ignore):
    """
    GIVEN schema and expected dict_ignore
    WHEN dict_ignore is called with the schema
    THEN the expected dict_ignore is returned.
    """
    returned_dict_ignore = helpers.peek.dict_ignore(schema=schema, schemas={})

    assert returned_dict_ignore == expected_dict_ignore
