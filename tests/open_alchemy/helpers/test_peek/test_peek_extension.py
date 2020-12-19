"""Tests for peek helpers."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


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
    "prefix",
    [pytest.param(p, id=p) for p in helpers.peek.VALID_PREFIXES],
)
@pytest.mark.parametrize(
    "key_values, func, expected_value",
    [
        *(
            pytest.param(
                [(extension, value)],
                getattr(helpers.peek, extension.replace("-", "_")),
                expected,
                id=f"valid {extension}",
            )
            for extension, value, expected in [
                ("index", True, True),
                ("index", False, False),
                ("unique", True, True),
                ("unique", False, False),
                ("autoincrement", True, True),
                ("autoincrement", False, False),
                ("primary-key", True, True),
                ("primary-key", False, False),
                ("tablename", "table 1", "table 1"),
                ("tablename", "table 2", "table 2"),
                ("inherits", "Parent1", "Parent1"),
                ("inherits", True, True),
                ("json", True, True),
                ("backref", "table 1", "table 1"),
                ("secondary", "table 1", "table 1"),
                ("uselist", True, True),
                ("kwargs", {"key": "value"}, {"key": "value"}),
                ("foreign-key-kwargs", {"key": "value"}, {"key": "value"}),
                ("foreign-key", "id", "id"),
                ("foreign-key-column", "id", "id"),
                ("composite-index", ["id"], ["id"]),
                ("composite-unique", ["id"], ["id"]),
                ("server-default", "value 1", "value 1"),
                ("dict-ignore", True, True),
                ("dict-ignore", False, False),
            ]
        ),
        *(
            pytest.param(
                [],
                getattr(helpers.peek, extension.replace("-", "_")),
                None,
                id=f"{extension} missing",
            )
            for extension in [
                "index",
                "unique",
                "autoincrement",
                "primary-key",
                "tablename",
                "inherits",
                "json",
                "backref",
                "secondary",
                "uselist",
                "kwargs",
                "foreign-key-kwargs",
                "foreign-key",
                "foreign-key-column",
                "composite-index",
                "composite-unique",
                "server-default",
                "dict-ignore",
            ]
        ),
    ],
)
@pytest.mark.helper
def test_peek_value_func(prefix, key_values, func, expected_value):
    """
    GIVEN prefix, keys and values to build the schema and function to retrieve a value
    WHEN the function called with the schema
    THEN the expected value is returned.
    """
    schema = {f"{prefix}{key}": value for key, value in key_values}

    returned_value = func(schema=schema, schemas={})

    assert returned_value == expected_value


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in helpers.peek.VALID_PREFIXES],
)
@pytest.mark.parametrize(
    "key_values, func",
    [
        pytest.param(
            [(extension, value)],
            getattr(helpers.peek, extension.replace("-", "_")),
            id=f"invalid {extension}",
        )
        for extension, value in [
            ("autoincrement", "True"),
            ("index", "True"),
            ("unique", "True"),
            ("primary-key", "True"),
            ("tablename", True),
            ("inherits", 1),
            ("json", 1),
            ("backref", True),
            ("secondary", True),
            ("uselist", "True"),
            ("foreign-key", True),
            ("foreign-key-column", True),
            ("server-default", True),
            ("dict-ignore", "True"),
            ("kwargs", True),
            ("kwargs", {1: True}),
            ("kwargs", {1: True, "key": "value"}),
            ("kwargs", {"key": "value", 1: True}),
            ("kwargs", {1: True, 2: False}),
            ("foreign-key-kwargs", True),
            ("foreign-key-kwargs", {1: True}),
            ("foreign-key-kwargs", {1: True, "key": "value"}),
            ("foreign-key-kwargs", {"key": "value", 1: True}),
            ("foreign-key-kwargs", {1: True, 2: False}),
        ]
    ],
)
@pytest.mark.helper
def test_peek_malformed_schema_error(prefix, key_values, func):
    """
    GIVEN schema with an extension property defined as a string
    WHEN extension property is called with the schema
    THEN MalformedSchemaError is raised.
    """
    schema = {f"{prefix}{key}": value for key, value in key_values}

    with pytest.raises(exceptions.MalformedSchemaError):
        func(schema=schema, schemas={})


@pytest.mark.parametrize(
    "prefix",
    [pytest.param(p, id=p) for p in helpers.peek.VALID_PREFIXES],
)
@pytest.mark.parametrize(
    "key_values, func",
    [
        pytest.param(
            [(extension, value)],
            getattr(helpers.peek, extension.replace("-", "_")),
            id=f"invalid {extension}",
        )
        for extension, value in [
            ("mixins", "MissingDot"),
            ("mixins", ".second"),
            ("mixins", "first."),
            ("mixins", ".second.third"),
            ("mixins", "first..third"),
            ("mixins", "first.second."),
            ("mixins", ["first."]),
            ("mixins", ["first.", "first.second"]),
            ("mixins", ["first.second", ".second"]),
            ("mixins", ["first.", ".second"]),
            ("composite-index", True),
            ("composite-unique", True),
        ]
    ],
)
@pytest.mark.helper
def test_peek_malformed_extension_property_error(prefix, key_values, func):
    """
    GIVEN schema with an extension property defined as a string
    WHEN extension property is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    schema = {f"{prefix}{key}": value for key, value in key_values}

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        func(schema=schema, schemas={})
