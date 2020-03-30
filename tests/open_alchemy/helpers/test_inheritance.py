"""Tests for inheritance helpers."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas, exception",
    [
        ({"$ref": "#/components/schemas/Parent"}, {}, exceptions.SchemaNotFoundError),
        ({"allOf": "Parent"}, {}, exceptions.MalformedSchemaError),
        (
            {"allOf": [{"$ref": "#/components/schemas/Parent"}]},
            {},
            exceptions.SchemaNotFoundError,
        ),
    ],
    ids=[
        "$ref with parent that is not in schemas",
        "allOf not list",
        "allOf $ref with parent that is not in schemas",
    ],
)
@pytest.mark.helper
def test_check_parent_invalid(schema, schemas, exception):
    """
    GIVEN child and parent name, schemas and expected exception
    WHEN check_parent is called with the names and schemas
    THEN the expected exception is raised.
    """
    parent_name = "Parent"

    with pytest.raises(exception):
        helpers.inheritance.check_parent(
            schema=schema, parent_name=parent_name, schemas=schemas
        )


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    [
        ({}, {}, False),
        (
            {"$ref": "#/components/schemas/Parent"},
            {"Parent": {"x-tablename": "table 1"}},
            True,
        ),
        ({"$ref": "#/components/schemas/Parent"}, {"Parent": {}}, False),
        (
            {"$ref": "#/components/schemas/Intermediate"},
            {
                "Intermediate": {"$ref": "#/components/schemas/Parent"},
                "Parent": {"x-tablename": "table 1"},
            },
            True,
        ),
        (
            {"$ref": "#/components/schemas/Intermediate"},
            {"Intermediate": {"$ref": "#/components/schemas/Parent"}, "Parent": {}},
            False,
        ),
        (
            {"$ref": "#/components/schemas/Intermediate1"},
            {
                "Intermediate1": {"$ref": "#/components/schemas/Intermediate2"},
                "Intermediate2": {"$ref": "#/components/schemas/Parent"},
                "Parent": {"x-tablename": "table 1"},
            },
            True,
        ),
        (
            {"$ref": "#/components/schemas/Intermediate1"},
            {
                "Intermediate1": {"$ref": "#/components/schemas/Intermediate2"},
                "Intermediate2": {"$ref": "#/components/schemas/Parent"},
                "Parent": {},
            },
            False,
        ),
        ({"allOf": []}, {}, False),
        (
            {"allOf": [{"$ref": "#/components/schemas/Parent"}]},
            {"Parent": {"x-tablename": "table 1"}},
            True,
        ),
        ({"allOf": [{"$ref": "#/components/schemas/Parent"}]}, {"Parent": {}}, False),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent"},
                    {"$ref": "#/components/schemas/Other"},
                ]
            },
            {"Parent": {"x-tablename": "table 1"}, "Other": {}},
            True,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Other"},
                    {"$ref": "#/components/schemas/Parent"},
                ]
            },
            {"Parent": {"x-tablename": "table 1"}, "Other": {}},
            True,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Other1"},
                    {"$ref": "#/components/schemas/Other2"},
                ]
            },
            {"Other1": {}, "Other2": {}},
            False,
        ),
    ],
    ids=[
        "base empty",
        "base name match constructible",
        "base name match not constructible",
        "recursive single $ref constructable",
        "recursive single $ref not constructable",
        "recursive multiple $ref constructable",
        "recursive multiple $ref not constructable",
        "recursive allOf empty",
        "recursive allOf single constructible",
        "recursive allOf single not constructible",
        "recursive allOf multiple first constructible",
        "recursive allOf multiple second constructible",
        "recursive allOf multiple not constructible",
    ],
)
@pytest.mark.helper
def test_check_parent(schema, schemas, expected_result):
    """
    GIVEN child and parent schemas
    WHEN check_parent is called with the child and parent name and schemas
    THEN the expected result is returned.
    """
    parent_name = "Parent"

    result = helpers.inheritance.check_parent(
        schema=schema, parent_name=parent_name, schemas=schemas
    )

    assert result == expected_result
