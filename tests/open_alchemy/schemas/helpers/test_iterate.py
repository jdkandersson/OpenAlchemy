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
        pytest.param({"Schema1": {}, "Schema2": {},}, [], id="multiple none"),
        pytest.param(
            {"Schema1": {"x-tablename": "table 1"}, "Schema2": {},},
            [("Schema1", {"x-tablename": "table 1"}),],
            id="multiple first",
        ),
        pytest.param(
            {"Schema1": {}, "Schema2": {"x-tablename": "table 2"},},
            [("Schema2", {"x-tablename": "table 2"}),],
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
        pytest.param({}, {}, [], id="no properties"),
        pytest.param({"properties": {}}, {}, [], id="empty properties"),
        pytest.param(
            {"properties": {"prop_1": "value 1"}},
            {},
            [("prop_1", "value 1")],
            id="single property",
        ),
        pytest.param(
            {"properties": {"prop_1": "value 1", "prop_2": "value 2"}},
            {},
            [("prop_1", "value 1"), ("prop_2", "value 2")],
            id="multiple property",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"properties": {"prop_1": "value 1"}}},
            [("prop_1", "value 1")],
            id="$ref",
        ),
        pytest.param({"allOf": []}, {}, [], id="allOf empty"),
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
