"""Test for iterate helpers."""

import pytest

from open_alchemy.schemas.helpers import iterate


@pytest.mark.parametrize(
    "schemas, expected_schemas",
    [
        pytest.param({}, [], id="empty"),
        pytest.param({"Schema1": {}}, [], id="single not"),
        pytest.param(
            {"Schema1": {"x-tablename": "table 1"}},
            [("Schema1", {"x-tablename": "table 1"})],
            id="single is",
        ),
        pytest.param({"Schema1": {}, "Schema2": {}}, [], id="multiple none"),
        pytest.param(
            {"Schema1": {"x-tablename": "table 1"}, "Schema2": {}},
            [("Schema1", {"x-tablename": "table 1"})],
            id="multiple first",
        ),
        pytest.param(
            {"Schema1": {}, "Schema2": {"x-tablename": "table 2"}},
            [("Schema2", {"x-tablename": "table 2"})],
            id="multiple last",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
            },
            [
                ("Schema1", {"x-tablename": "table 1"}),
                ("Schema2", {"x-tablename": "table 2"}),
            ],
            id="multiple all",
        ),
    ],
)
@pytest.mark.schemas
def test_constructable(schemas, expected_schemas):
    """
    GIVEN schemas and expected schemas
    WHEN constructable is called with the schemas
    THEN an iterable with all the names and schemas in the expected schemas are
        returned.
    """
    returned_schemas = iterate.constructable(schemas=schemas)

    assert list(returned_schemas) == expected_schemas


@pytest.mark.parametrize(
    "schema, schemas, expected_properties",
    [
        pytest.param(True, {}, [], id="not dict"),
        pytest.param({}, {}, [], id="no properties"),
        pytest.param({"properties": {}}, {}, [], id="empty properties"),
        pytest.param({"properties": True}, {}, [], id="properties not dictionary",),
        pytest.param(
            {"properties": {"prop_1": "value 1"}},
            {},
            [("prop_1", "value 1")],
            id="single property",
        ),
        pytest.param(
            {"x-inherits": False, "properties": {"prop_1": "value 1"}},
            {},
            [("prop_1", "value 1")],
            id="single property x-inherits False",
        ),
        pytest.param(
            {"properties": {"prop_1": "value 1", "prop_2": "value 2"}},
            {},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="multiple property",
        ),
        pytest.param({"$ref": True}, {}, [], id="$ref not string",),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"properties": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="$ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"}, {}, [], id="$ref not resolve",
        ),
        pytest.param({"allOf": True}, {}, [], id="allOf not list"),
        pytest.param({"allOf": []}, {}, [], id="allOf empty"),
        pytest.param({"allOf": [True]}, {}, [], id="allOf elements not dict"),
        pytest.param(
            {"allOf": [{"properties": {"prop_1": "value 1"}}]},
            {},
            [("prop_1", "value 1")],
            id="allOf single",
        ),
        pytest.param(
            {
                "allOf": [
                    {"properties": {"prop_1": "value 1"}},
                    {"properties": {"prop_2": "value 2"}},
                ]
            },
            {},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="allOf multiple",
        ),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"properties": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="allOf $ref",
        ),
    ],
)
@pytest.mark.schemas
def test_properties(schema, schemas, expected_properties):
    """
    GIVEN schema, schemas and expected properties
    WHEN properties is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_properties = iterate.properties(schema=schema, schemas=schemas)

    assert list(returned_properties) == expected_properties


@pytest.mark.parametrize(
    "schema, schemas, expected_properties",
    [
        pytest.param(
            {"x-inherits": 1, "properties": {"prop_1": "value 1"}},
            {},
            [],
            id="x-inherits causes MalformedSchemaError",
        ),
        pytest.param(
            {"x-inherits": "ParentSchema", "properties": {"prop_1": "value 1"}},
            {},
            [],
            id="x-inherits causes InheritanceError",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-inherits": "ParentSchema", "properties": {"prop_1": "value 1"}},
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {},
            [],
            id="x-inherits causes SchemaNotFoundError",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "x-inherits": "ParentSchema",
                        "x-tablename": "schema",
                        "properties": {"prop_1": "value 1"},
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {
                "ParentSchema": {
                    "x-tablename": "parent_schema",
                    "properties": {"prop_2": "value 2"},
                }
            },
            [("prop_1", "value 1")],
            id="skip",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-tablename": "schema", "properties": {"prop_1": "value 1"}},
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {
                "ParentSchema": {
                    "x-tablename": "parent_schema",
                    "properties": {"prop_2": "value 2"},
                }
            },
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="no inheritance not skip",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "properties": {"prop_1": "value 1"},
                        "x-inherits": "ParentSchema",
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {
                "ParentSchema": {
                    "x-tablename": "parent_schema",
                    "properties": {"prop_2": "value 2"},
                }
            },
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="single table not skip",
        ),
    ],
)
@pytest.mark.schemas
def test_properties_joined(schema, schemas, expected_properties):
    """
    GIVEN schema, schemas and expected properties
    WHEN properties is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_properties = iterate.properties(
        schema=schema, schemas=schemas, stay_within_tablename=True
    )

    assert list(returned_properties) == expected_properties


@pytest.mark.parametrize(
    "schema, schemas, expected_properties",
    [
        pytest.param(
            {
                "allOf": [
                    {
                        "x-inherits": "ParentSchema",
                        "x-tablename": "schema",
                        "properties": {"prop_1": "value 1"},
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {
                "ParentSchema": {
                    "x-tablename": "parent_schema",
                    "properties": {"prop_2": "value 2"},
                }
            },
            [("prop_1", "value 1")],
            id="skip",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "properties": {"prop_1": "value 1"},
                        "x-inherits": "ParentSchema",
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {
                "ParentSchema": {
                    "x-tablename": "parent_schema",
                    "properties": {"prop_2": "value 2"},
                }
            },
            [("prop_1", "value 1")],
            id="single table skip",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-tablename": "schema", "properties": {"prop_1": "value 1"}},
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {
                "ParentSchema": {
                    "x-tablename": "parent_schema",
                    "properties": {"prop_2": "value 2"},
                }
            },
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="no inheritance not skip",
        ),
    ],
)
@pytest.mark.schemas
def test_properties_single(schema, schemas, expected_properties):
    """
    GIVEN schema, schemas and expected properties
    WHEN properties is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_properties = iterate.properties(
        schema=schema, schemas=schemas, stay_within_model=True
    )

    assert list(returned_properties) == expected_properties


@pytest.mark.parametrize(
    "schema, schemas, expected_required_lists",
    [
        pytest.param(True, {}, [], id="not dict"),
        pytest.param({}, {}, [], id="no properties"),
        pytest.param({"properties": {}}, {}, [], id="empty properties"),
        pytest.param({"properties": True}, {}, [], id="properties not dictionary",),
        pytest.param(
            {"properties": {"prop_1": "value 1"}},
            {},
            [("prop_1", "value 1")],
            id="single property",
        ),
        pytest.param(
            {"x-inherits": False, "properties": {"prop_1": "value 1"}},
            {},
            [("prop_1", "value 1")],
            id="single property x-inherits False",
        ),
        pytest.param(
            {"properties": {"prop_1": "value 1", "prop_2": "value 2"}},
            {},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="multiple property",
        ),
        pytest.param({"$ref": True}, {}, [], id="$ref not string",),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"properties": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="$ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"}, {}, [], id="$ref not resolve",
        ),
        pytest.param({"allOf": True}, {}, [], id="allOf not list"),
        pytest.param({"allOf": []}, {}, [], id="allOf empty"),
        pytest.param({"allOf": [True]}, {}, [], id="allOf elements not dict"),
        pytest.param(
            {"allOf": [{"properties": {"prop_1": "value 1"}}]},
            {},
            [("prop_1", "value 1")],
            id="allOf single",
        ),
        pytest.param(
            {
                "allOf": [
                    {"properties": {"prop_1": "value 1"}},
                    {"properties": {"prop_2": "value 2"}},
                ]
            },
            {},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="allOf multiple",
        ),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"properties": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="allOf $ref",
        ),
    ],
)
@pytest.mark.schemas
def test_required_lists(schema, schemas, expected_required_lists):
    """
    GIVEN schema, schemas and expected required lists
    WHEN required_lists is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_required_lists = iterate.required_lists(schema=schema, schemas=schemas)

    assert list(returned_required_lists) == expected_required_lists
