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
    schema = {"x-openalchemy-autoincrement": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.autoincrement(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_autoincrement",
    [
        ({}, None),
        ({"x-autoincrement": True}, True),
        ({"x-autoincrement": False}, False),
        ({"x-openalchemy-autoincrement": True}, True),
        ({"x-openalchemy-autoincrement": False}, False),
    ],
    # ids=["missing", "true", "false"],
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


@pytest.mark.helper
def test_index_wrong_type():
    """
    GIVEN schema with index defined as a string
    WHEN index is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-index": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.index(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_index",
    [({}, None), ({"x-index": True}, True), ({"x-index": False}, False)],
    ids=["missing", "true", "false"],
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


@pytest.mark.helper
def test_unique_wrong_type():
    """
    GIVEN schema with unique defined as a string
    WHEN unique is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-unique": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.unique(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_unique",
    [({}, None), ({"x-unique": True}, True), ({"x-unique": False}, False)],
    ids=["missing", "true", "false"],
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


@pytest.mark.helper
def test_primary_key_wrong_type():
    """
    GIVEN schema with primary key defined as a string
    WHEN primary_key is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-primary-key": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.primary_key(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_primary_key",
    [
        pytest.param({}, None, id="missing"),
        pytest.param({"x-primary-key": False}, False, id="False"),
        pytest.param({"x-primary-key": True}, True, id="True"),
    ],
    ids=["missing", "false", "true"],
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


@pytest.mark.helper
def test_tablename_wrong_type():
    """
    GIVEN schema with tablename defined as a boolean
    WHEN tablename is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-tablename": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.tablename(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_tablename",
    [({}, None), ({"x-tablename": "table 1"}, "table 1")],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_inherits_wrong_type():
    """
    GIVEN schema with x-inherits defined as an integer
    WHEN inherits is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-inherits": 1}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.inherits(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_inherits",
    [({}, None), ({"x-inherits": "Parent1"}, "Parent1"), ({"x-inherits": True}, True)],
    ids=["missing", "defined string", "defined boolean"],
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


@pytest.mark.helper
def test_json_wrong_type():
    """
    GIVEN schema with x-json defined as an integer
    WHEN json is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-json": 1}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.json(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_json",
    [({}, None), ({"x-json": True}, True)],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_backref_wrong_type():
    """
    GIVEN schema with backref defined as a boolean
    WHEN backref is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-backref": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.backref(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_backref",
    [({}, None), ({"x-backref": "table 1"}, "table 1")],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_secondary_wrong_type():
    """
    GIVEN schema with secondary defined as a boolean
    WHEN secondary is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-secondary": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.secondary(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_secondary",
    [({}, None), ({"x-secondary": "table 1"}, "table 1")],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_uselist_wrong_type():
    """
    GIVEN schema with uselist defined as a boolean
    WHEN uselist is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-uselist": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.uselist(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_uselist",
    [({}, None), ({"x-uselist": True}, True)],
    ids=["missing", "defined"],
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
    [({}, None), ({"x-kwargs": {"key": "value"}}, {"key": "value"})],
    ids=["missing", "defined"],
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
    [({}, None), ({"x-foreign-key-kwargs": {"key": "value"}}, {"key": "value"})],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_foreign_key_wrong_type():
    """
    GIVEN schema with foreign-key defined as a boolean
    WHEN foreign_key is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-foreign-key": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.foreign_key(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_foreign_key",
    [({}, None), ({"x-foreign-key": "id"}, "id")],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_foreign_key_column_wrong_type():
    """
    GIVEN schema with foreign-key-column defined as a boolean
    WHEN foreign_key_column is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-foreign-key-column": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.foreign_key_column(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_foreign_key_column",
    [({}, None), ({"x-foreign-key-column": "id"}, "id")],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_composite_index_wrong_type():
    """
    GIVEN schema with composite-index defined as a boolean
    WHEN composite_index is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    schema = {"x-composite-index": True}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.peek.composite_index(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_composite_index",
    [({}, None), ({"x-composite-index": ["id"]}, ["id"])],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_composite_unique_wrong_type():
    """
    GIVEN schema with composite-unique defined as a boolean
    WHEN composite_unique is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    schema = {"x-composite-unique": True}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        helpers.peek.composite_unique(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_composite_unique",
    [({}, None), ({"x-composite-unique": ["id"]}, ["id"])],
    ids=["missing", "defined"],
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


@pytest.mark.helper
def test_server_default_wrong_type():
    """
    GIVEN schema with server_default defined as a string
    WHEN server_default is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-server-default": True}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.server_default(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_server_default",
    [
        pytest.param({}, None, id="missing"),
        pytest.param({"x-server-default": "value 1"}, "value 1", id="defined"),
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


@pytest.mark.helper
def test_dict_ignore_wrong_type():
    """
    GIVEN schema with dict_ignore defined as a string
    WHEN dict_ignore is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {"x-dict-ignore": "True"}

    with pytest.raises(exceptions.MalformedSchemaError):
        helpers.peek.dict_ignore(schema=schema, schemas={})


@pytest.mark.parametrize(
    "schema, expected_dict_ignore",
    [
        ({}, None),
        ({"x-dict-ignore": True}, True),
        ({"x-dict-ignore": False}, False),
    ],
    ids=["missing", "true", "false"],
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
