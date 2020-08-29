"""Tests for process helpers."""

import pytest

from open_alchemy.schemas.helpers import process

GET_ARTIFACTS_TESTS = [
    pytest.param(
        {},
        [],
        id="empty",
    ),
    pytest.param(
        {"Schema1": {}},
        [],
        id="single schema not constructable",
    ),
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
    "schemas, expected_artifacts",
    GET_ARTIFACTS_TESTS,
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

    returned_artifacts = process.get_artifacts(
        schemas=schemas, get_schema_artifacts=get_artifacts_func
    )

    assert list(returned_artifacts) == expected_artifacts


TArt = process.TArtifacts


CALCULATE_OUTPUTS_TESTS = [
    pytest.param(
        [],
        [],
        id="empty",
    ),
    pytest.param(
        [TArt("Schema1", "prop_1", {})],
        [
            (
                "Schema1",
                "[TArtifacts(schema_name='Schema1', property_name='prop_1', "
                "property_schema={})]",
            )
        ],
        id="single",
    ),
    pytest.param(
        [TArt("Schema1", "prop_1", {}), TArt("Schema2", "prop_1", {})],
        [
            (
                "Schema1",
                "[TArtifacts(schema_name='Schema1', property_name='prop_1', "
                "property_schema={})]",
            ),
            (
                "Schema2",
                "[TArtifacts(schema_name='Schema2', property_name='prop_1', "
                "property_schema={})]",
            ),
        ],
        id="multiple different",
    ),
    pytest.param(
        [
            TArt("Schema1", "prop_1", {}),
            TArt("Schema1", "prop_2", {}),
            TArt("Schema2", "prop_1", {}),
        ],
        [
            (
                "Schema1",
                "[TArtifacts(schema_name='Schema1', property_name='prop_1', "
                "property_schema={}), TArtifacts(schema_name='Schema1', "
                "property_name='prop_2', property_schema={})]",
            ),
            (
                "Schema2",
                "[TArtifacts(schema_name='Schema2', property_name='prop_1', "
                "property_schema={})]",
            ),
        ],
        id="multiple some different first multiple ordered",
    ),
    pytest.param(
        [
            TArt("Schema1", "prop_1", {}),
            TArt("Schema2", "prop_1", {}),
            TArt("Schema1", "prop_2", {}),
        ],
        [
            (
                "Schema1",
                "[TArtifacts(schema_name='Schema1', property_name='prop_1', "
                "property_schema={}), TArtifacts(schema_name='Schema1', "
                "property_name='prop_2', property_schema={})]",
            ),
            (
                "Schema2",
                "[TArtifacts(schema_name='Schema2', property_name='prop_1', "
                "property_schema={})]",
            ),
        ],
        id="multiple some different first multiple not ordered",
    ),
    pytest.param(
        [
            TArt("Schema1", "prop_1", {}),
            TArt("Schema2", "prop_1", {}),
            TArt("Schema2", "prop_2", {}),
        ],
        [
            (
                "Schema1",
                "[TArtifacts(schema_name='Schema1', property_name='prop_1', "
                "property_schema={})]",
            ),
            (
                "Schema2",
                "[TArtifacts(schema_name='Schema2', property_name='prop_1', "
                "property_schema={}), TArtifacts(schema_name='Schema2', "
                "property_name='prop_2', property_schema={})]",
            ),
        ],
        id="multiple some different second multiple",
    ),
    pytest.param(
        [TArt("Schema1", "prop_1", {}), TArt("Schema1", "prop_2", {})],
        [
            (
                "Schema1",
                "[TArtifacts(schema_name='Schema1', property_name='prop_1', "
                "property_schema={}), TArtifacts(schema_name='Schema1', "
                "property_name='prop_2', property_schema={})]",
            )
        ],
        id="multiple same",
    ),
]


@pytest.mark.parametrize("artifacts, expected_outputs", CALCULATE_OUTPUTS_TESTS)
@pytest.mark.schemas
def test_calculate_outputs(artifacts, expected_outputs):
    """
    GIVEN artifacts and expected outputs
    WHEN calculate_outputs is called with the artifacts and a function that returns the
        input as a string
    THEN the expected outputs are returned.
    """
    returned_artifacts = process.calculate_outputs(
        artifacts=artifacts, calculate_output=lambda arg: str(list(arg))
    )

    assert list(returned_artifacts) == expected_outputs
