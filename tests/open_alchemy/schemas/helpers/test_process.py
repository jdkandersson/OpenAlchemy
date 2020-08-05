"""Tests for process helpers."""

import pytest

from open_alchemy.schemas.helpers import process

GET_ARTIFACTS_TESTS = [
    pytest.param({}, [], id="empty",),
    pytest.param({"Schema1": {}}, [], id="single schema not constructable",),
    pytest.param(
        {"Schema1": {"x-tablename": "schema_1", "properties": {}}},
        [],
        id="single schema no properties",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"key_1": "value 1"}},
            }
        },
        [("{'Schema1'", "Schema1", "prop_1", {"key_1": "value 1"})],
        id="single schema single property",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {"key_1": "value 1"},
                    "prop_2": {"key_2": "value 2"},
                },
            }
        },
        [
            ("{'Schema1'", "Schema1", "prop_1", {"key_1": "value 1"}),
            ("{'Schema1'", "Schema1", "prop_2", {"key_2": "value 2"}),
        ],
        id="single schema multiple property",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"key_1": "value 1"}},
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {"prop_2": {"key_2": "value 2"}},
            },
        },
        [
            ("{'Schema1'", "Schema1", "prop_1", {"key_1": "value 1"}),
            ("{'Schema1'", "Schema2", "prop_2", {"key_2": "value 2"}),
        ],
        id="multiple schema",
    ),
]


@pytest.mark.parametrize(
    "schemas, expected_artifacts", GET_ARTIFACTS_TESTS,
)
@pytest.mark.schemas
def test_get_artifacts(schemas, expected_artifacts):
    """
    GIVEN schemas and expected artifacts
    WHEN get_artifacts is called with the schemas and a function that returns the input
    THEN the expected artifacts are returned.
    """

    def get_artifacts_func(schemas, schema_name, schema):
        """Helper function for each schema."""
        schemas_str = str(schemas)[:10]

        return map(
            lambda args: (schemas_str, schema_name, *args), schema["properties"].items()
        )

    returned_artifacts = list(
        process.get_artifacts(schemas=schemas, get_schema_artifacts=get_artifacts_func)
    )

    assert list(returned_artifacts) == expected_artifacts
