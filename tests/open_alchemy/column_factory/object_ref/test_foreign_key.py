"""Tests for foreign key module."""

import pytest

from open_alchemy import exceptions
from open_alchemy.column_factory.object_ref import foreign_key


@pytest.mark.parametrize(
    "model_schema",
    [
        {
            "properties": {
                "ref_table_fk_column": {"x-foreign-key": "ref_table.fk_column"}
            }
        },
        {
            "properties": {
                "ref_table_fk_column": {
                    "type": "not_fk_type",
                    "x-foreign-key": "ref_table.fk_column",
                }
            }
        },
        {"properties": {"ref_table_fk_column": {"type": "fk_type"}}},
        {
            "properties": {
                "ref_table_fk_column": {
                    "type": "fk_type",
                    "x-foreign-key": "wrong_table.wrong_column",
                }
            }
        },
    ],
    ids=["no type", "wrong type", "no x-foreign-key", "wrong x-foreign-key"],
)
@pytest.mark.column
def test_check_required_invalid_schema(model_schema):
    """
    GIVEN model schema that is not valid
    WHEN check_required is called
    THEN MalformedRelationshipError is raised.
    """
    fk_spec = {"type": "fk_type", "x-foreign-key": "ref_table.fk_column"}
    fk_logical_name = "ref_table_fk_column"

    with pytest.raises(exceptions.MalformedRelationshipError):
        foreign_key.check_required(
            fk_spec=fk_spec,
            fk_logical_name=fk_logical_name,
            model_schema=model_schema,
            schemas={},
        )


@pytest.mark.parametrize(
    "model_schema, schemas, expected_required",
    [
        ({"properties": {}}, {}, True),
        (
            {
                "properties": {
                    "ref_table_fk_column": {
                        "type": "fk_type",
                        "x-foreign-key": "ref_table.fk_column",
                    }
                }
            },
            {},
            False,
        ),
        (
            {
                "properties": {
                    "ref_table_fk_column": {"$ref": "#/components/schemas/FkSchema"}
                }
            },
            {"FkSchema": {"type": "fk_type", "x-foreign-key": "ref_table.fk_column"}},
            False,
        ),
        (
            {
                "properties": {
                    "ref_table_fk_column": {
                        "allOf": [
                            {"type": "fk_type", "x-foreign-key": "ref_table.fk_column"}
                        ]
                    }
                }
            },
            {},
            False,
        ),
    ],
    ids=[
        "not in model schema",
        "in model schema",
        "in model schema $ref",
        "in model schema allOf",
    ],
)
@pytest.mark.column
def test_check_required(model_schema, schemas, expected_required):
    """
    GIVEN foreign key spec, foreign key logical name, model schema, schemas and
        expected required
    WHEN check_required is called
    THEN the expected required is returned.
    """
    fk_spec = {"type": "fk_type", "x-foreign-key": "ref_table.fk_column"}
    fk_logical_name = "ref_table_fk_column"

    required = foreign_key.check_required(
        fk_spec=fk_spec,
        fk_logical_name=fk_logical_name,
        model_schema=model_schema,
        schemas=schemas,
    )

    assert required == expected_required
