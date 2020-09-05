"""Test for iterate helpers."""

import pytest

from open_alchemy.schemas.helpers import iterate


@pytest.mark.parametrize(
    "schemas, expected_schemas",
    [
        pytest.param({}, [], id="empty"),
        pytest.param({"Schema1": {}}, [], id="single not"),
        pytest.param(
            {"Schema1": {"x-tablename": True}},
            [("Schema1", {"x-tablename": True})],
            id="single malformed tablename",
        ),
        pytest.param(
            {"Schema1": {"x-inherits": 1}},
            [("Schema1", {"x-inherits": 1})],
            id="single malformed inherits",
        ),
        pytest.param(
            {"Schema1": {"allOf": [{"$ref": "#/components/schemas/Schema2"}, {}]}},
            [],
            id="single missing reference",
        ),
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
@pytest.mark.helper
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
    "schemas, expected_schemas",
    [
        pytest.param({}, [], id="empty"),
        pytest.param({"Schema1": {}}, [("Schema1", {})], id="single not"),
        pytest.param(
            {"Schema1": {"x-tablename": True}},
            [],
            id="single tablename",
        ),
        pytest.param(
            {"Schema1": {"x-inherits": 1}},
            [],
            id="single inherits",
        ),
        pytest.param(
            {"Schema1": {"allOf": [{"$ref": "#/components/schemas/Schema2"}, {}]}},
            [],
            id="single missing reference",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table 1"},
                "Schema2": {"x-tablename": "table 2"},
            },
            [],
            id="multiple all",
        ),
        pytest.param(
            {"Schema1": {}, "Schema2": {"x-tablename": "table 2"}},
            [("Schema1", {})],
            id="multiple last",
        ),
        pytest.param(
            {"Schema1": {"x-tablename": "table 1"}, "Schema2": {}},
            [("Schema2", {})],
            id="multiple first",
        ),
        pytest.param(
            {"Schema1": {}, "Schema2": {}},
            [("Schema1", {}), ("Schema2", {})],
            id="multiple none",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.helper
def test_not_constructable(schemas, expected_schemas):
    """
    GIVEN schemas and expected schemas
    WHEN not_constructable is called with the schemas
    THEN an iterable with all the names and schemas in the expected schemas are
        returned.
    """
    returned_schemas = iterate.not_constructable(schemas=schemas)

    assert list(returned_schemas) == expected_schemas


@pytest.mark.parametrize(
    "schema, schemas, expected_properties",
    [
        pytest.param(True, {}, [], id="not dict"),
        pytest.param({}, {}, [], id="no properties"),
        pytest.param({"properties": {}}, {}, [], id="empty properties"),
        pytest.param(
            {"properties": True},
            {},
            [],
            id="properties not dictionary",
        ),
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
        pytest.param(
            {"$ref": True},
            {},
            [],
            id="$ref not string",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"properties": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="$ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {},
            [],
            id="$ref not resolve",
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
            {"allOf": [{"properties": True}, {"properties": {"prop_2": "value 2"}}]},
            {},
            [("prop_2", "value 2")],
            id="allOf multiple first not dict",
        ),
        pytest.param(
            {"allOf": [{"properties": {"prop_1": "value 1"}}, {"properties": True}]},
            {},
            [("prop_1", "value 1")],
            id="allOf multiple second not dict",
        ),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"properties": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="allOf $ref",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema1"},
                    {"$ref": "#/components/schemas/RefSchema2"},
                ]
            },
            {
                "RefSchema1": {"properties": {"prop_1": "value 1"}},
                "RefSchema2": {"properties": {"prop_2": "value 2"}},
            },
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="allOf multiple $ref",
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
            id="allOf multiple local",
        ),
        pytest.param(
            {
                "allOf": [
                    {"properties": {"prop_1": "value 1"}},
                    {"$ref": "#/components/schemas/RefSchema"},
                ]
            },
            {"RefSchema": {"properties": {"prop_2": "value 2"}}},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="allOf local and $ref local first",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"properties": {"prop_1": "value 1"}},
                ]
            },
            {"RefSchema": {"properties": {"prop_2": "value 2"}}},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="allOf local and $ref $ref first",
        ),
        pytest.param(
            {
                "allOf": [
                    {"properties": {"prop_1": "value 1"}},
                    {"properties": {"prop_1": "value 2"}},
                ]
            },
            {},
            [("prop_1", "value 1")],
            id="allOf multiple duplicate",
        ),
        pytest.param(
            {
                "allOf": [
                    {"properties": {"prop_1": "value 1"}},
                    {"$ref": "#/components/schemas/RefSchema"},
                ]
            },
            {"RefSchema": {"properties": {"prop_1": "value 2"}}},
            [("prop_1", "value 1")],
            id="allOf local and $ref local first duplicate",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"properties": {"prop_1": "value 1"}},
                ]
            },
            {"RefSchema": {"properties": {"prop_1": "value 2"}}},
            [("prop_1", "value 1")],
            id="allOf local and $ref $ref first duplicate",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.helper
def test_properties_items(schema, schemas, expected_properties):
    """
    GIVEN schema, schemas and expected properties
    WHEN properties is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_properties = iterate.properties_items(schema=schema, schemas=schemas)

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
@pytest.mark.helper
def test_properties_joined(schema, schemas, expected_properties):
    """
    GIVEN schema, schemas and expected properties
    WHEN properties is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_properties = iterate.properties_items(
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
@pytest.mark.helper
def test_properties_single(schema, schemas, expected_properties):
    """
    GIVEN schema, schemas and expected properties
    WHEN properties is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_properties = iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )

    assert list(returned_properties) == expected_properties


@pytest.mark.parametrize(
    "schema, schemas, expected_required_values",
    [
        pytest.param({}, {}, [], id="no required"),
        pytest.param(
            {"required": "value 1"},
            {},
            ["value 1"],
            id="single required",
        ),
        pytest.param(
            {"x-inherits": False, "required": "value 1"},
            {},
            ["value 1"],
            id="single required x-inherits False",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"required": "value 1"}},
            ["value 1"],
            id="$ref",
        ),
        pytest.param(
            {"allOf": [{"required": "value 1"}]},
            {},
            ["value 1"],
            id="allOf single",
        ),
        pytest.param(
            {"allOf": [{"required": "value 1"}, {"required": "value 2"}]},
            {},
            ["value 1", "value 2"],
            id="allOf multiple",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.helper
def test_required_values(schema, schemas, expected_required_values):
    """
    GIVEN schema, schemas and expected required lists
    WHEN required_values is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_required_values = iterate.required_values(schema=schema, schemas=schemas)

    assert list(returned_required_values) == expected_required_values


@pytest.mark.parametrize(
    "schema, schemas, expected_required_values",
    [
        pytest.param(
            {"x-inherits": 1, "required": "value 1"},
            {},
            [],
            id="x-inherits causes MalformedSchemaError",
        ),
        pytest.param(
            {"x-inherits": "ParentSchema", "required": "value 1"},
            {},
            [],
            id="x-inherits causes InheritanceError",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-inherits": "ParentSchema", "required": "value 1"},
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
                        "required": "value 1",
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {"ParentSchema": {"x-tablename": "parent_schema", "required": "value 2"}},
            ["value 1"],
            id="skip",
        ),
        pytest.param(
            {
                "allOf": [
                    {"required": "value 1", "x-inherits": "ParentSchema"},
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {"ParentSchema": {"x-tablename": "parent_schema", "required": "value 2"}},
            ["value 1"],
            id="single table skip",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-tablename": "schema", "required": "value 1"},
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {"ParentSchema": {"x-tablename": "parent_schema", "required": "value 2"}},
            ["value 1", "value 2"],
            id="no inheritance not skip",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.helper
def test_required_values_single(schema, schemas, expected_required_values):
    """
    GIVEN schema, schemas and expected required lists
    WHEN required_values is called with the schema and schemas and
        stay_within_model set
    THEN the expected name and property schema are returned.
    """
    returned_required_values = iterate.required_values(
        schema=schema, schemas=schemas, stay_within_model=True
    )

    assert list(returned_required_values) == expected_required_values


@pytest.mark.parametrize(
    "schema, schemas, expected_values",
    [
        pytest.param({"required": True}, {}, [], id="required not list"),
        pytest.param({"required": []}, {}, [], id="required empty"),
        pytest.param({"required": ["value 1"]}, {}, ["value 1"], id="required single"),
        pytest.param(
            {"required": ["value 1", "value 2"]},
            {},
            ["value 1", "value 2"],
            id="required multiple",
        ),
        pytest.param(
            {"allOf": [{"required": ["value 1"]}, {"required": ["value 2"]}]},
            {},
            ["value 1", "value 2"],
            id="multiple required single",
        ),
        pytest.param(
            {"allOf": [{"required": True}, {"required": ["value 2"]}]},
            {},
            ["value 2"],
            id="multiple required first not list",
        ),
        pytest.param(
            {"allOf": [{"required": ["value 1"]}, {"required": True}]},
            {},
            ["value 1"],
            id="multiple required second not list",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.helper
def test_required_items(schema, schemas, expected_values):
    """
    GIVEN schema, schemas and expected values
    WHEN required_items is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_values = iterate.required_items(schema=schema, schemas=schemas)

    assert list(returned_values) == expected_values


@pytest.mark.parametrize(
    "schema, schemas, expected_values",
    [
        pytest.param(
            {
                "allOf": [
                    {"required": ["value 1"], "x-inherits": "ParentSchema"},
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {
                "ParentSchema": {
                    "x-tablename": "parent_schema",
                    "required": ["value 2"],
                }
            },
            ["value 1"],
            id="single table skip",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-tablename": "schema", "required": ["value 1"]},
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {
                "ParentSchema": {
                    "x-tablename": "parent_schema",
                    "required": ["value 2"],
                }
            },
            ["value 1", "value 2"],
            id="no inheritance not skip",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.helper
def test_required_items_single(schema, schemas, expected_values):
    """
    GIVEN schema, schemas and expected values
    WHEN required_items is called with the schema and schemas and
        stay_within_model set
    THEN the expected name and property schema are returned.
    """
    returned_values = iterate.required_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )

    assert list(returned_values) == expected_values


@pytest.mark.parametrize(
    "schema, schemas, expected_backrefs",
    [
        pytest.param(True, {}, [], id="not dict"),
        pytest.param({}, {}, [], id="no backrefs"),
        pytest.param({"x-backrefs": {}}, {}, [], id="empty backrefs"),
        pytest.param(
            {"x-backrefs": True},
            {},
            [],
            id="backrefs not dictionary",
        ),
        pytest.param(
            {"x-backrefs": {"prop_1": "value 1"}},
            {},
            [("prop_1", "value 1")],
            id="single property",
        ),
        pytest.param(
            {"x-backrefs": {"prop_1": "value 1", "prop_2": "value 2"}},
            {},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="multiple property",
        ),
        pytest.param(
            {"$ref": True},
            {},
            [],
            id="$ref not string",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-backrefs": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="$ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {},
            [],
            id="$ref not resolve",
        ),
        pytest.param({"allOf": True}, {}, [], id="allOf not list"),
        pytest.param({"allOf": []}, {}, [], id="allOf empty"),
        pytest.param({"allOf": [True]}, {}, [], id="allOf elements not dict"),
        pytest.param(
            {"allOf": [{"x-backrefs": {"prop_1": "value 1"}}]},
            {},
            [("prop_1", "value 1")],
            id="allOf single",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-backrefs": {"prop_1": "value 1"}},
                    {"x-backrefs": {"prop_2": "value 2"}},
                ]
            },
            {},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="allOf multiple",
        ),
        pytest.param(
            {"allOf": [{"x-backrefs": True}, {"x-backrefs": {"prop_2": "value 2"}}]},
            {},
            [("prop_2", "value 2")],
            id="allOf multiple first not dict",
        ),
        pytest.param(
            {"allOf": [{"x-backrefs": {"prop_1": "value 1"}}, {"x-backrefs": True}]},
            {},
            [("prop_1", "value 1")],
            id="allOf multiple second not dict",
        ),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"x-backrefs": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="allOf $ref",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-backrefs": {"prop_1": "value 1"}},
                    {"x-backrefs": {"prop_1": "value 2"}},
                ]
            },
            {},
            [("prop_1", "value 1")],
            id="allOf duplicates",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.helper
def test_backrefs_items(schema, schemas, expected_backrefs):
    """
    GIVEN schema, schemas and expected backrefs
    WHEN backrefs is called with the schema and schemas
    THEN the expected name and property schema are returned.
    """
    returned_backrefs = iterate.backrefs_items(schema=schema, schemas=schemas)

    assert list(returned_backrefs) == expected_backrefs
