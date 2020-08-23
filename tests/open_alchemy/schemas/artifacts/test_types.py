"""Tests for types."""

import pytest

from open_alchemy.schemas import artifacts


@pytest.mark.parametrize(
    "artifacts_value, expected_dict",
    [
        pytest.param(
            artifacts.types.ModelArtifacts(
                tablename="table_1",
                inherits=None,
                parent=None,
                description=None,
                mixins=None,
                kwargs=None,
                composite_index=None,
                composite_unique=None,
            ),
            {"tablename": "table_1"},
            id="opt values None",
        ),
        pytest.param(
            artifacts.types.ModelArtifacts(
                tablename="table_1",
                inherits=True,
                parent="Parent1",
                description="description 1",
                mixins=["model.Mixin1"],
                kwargs={"key": "value"},
                composite_index=[{"expressions": ["column_1"]}],
                composite_unique=[{"columns": ["column_1"]}],
            ),
            {
                "tablename": "table_1",
                "inherits": True,
                "parent": "Parent1",
                "description": "description 1",
                "mixins": ["model.Mixin1"],
                "kwargs": {"key": "value"},
                "composite_index": [{"expressions": ["column_1"]}],
                "composite_unique": [{"columns": ["column_1"]}],
            },
            id="opt values defined",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_model_artifacts(artifacts_value, expected_dict):
    """
    GIVEN artifacts and expected dictionary
    WHEN to_dict is called on the artifacts
    THEN the expected dictionary is returned.
    """
    returned_dict = artifacts_value.to_dict()

    assert returned_dict == expected_dict
