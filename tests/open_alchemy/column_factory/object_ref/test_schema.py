"""Tests for _calculate_schema."""
# pylint: disable=protected-access

import pytest

from open_alchemy import types
from open_alchemy.column_factory import object_ref


@pytest.mark.parametrize(
    "artifacts, expected_schema",
    [
        pytest.param(
            types.ObjectArtifacts(
                spec={},
                logical_name="logical name 1",
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
            ),
            {"type": "object", "x-de-$ref": "RefSchema"},
            id="plain",
        ),
        pytest.param(
            types.ObjectArtifacts(
                spec={},
                logical_name="logical name 1",
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                nullable=True,
            ),
            {"type": "object", "x-de-$ref": "RefSchema", "nullable": True},
            id="nullable True",
        ),
        pytest.param(
            types.ObjectArtifacts(
                spec={},
                logical_name="logical name 1",
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                nullable=False,
            ),
            {"type": "object", "x-de-$ref": "RefSchema", "nullable": False},
            id="nullable False",
        ),
        pytest.param(
            types.ObjectArtifacts(
                spec={},
                logical_name="logical name 1",
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                description="description 1",
            ),
            {
                "type": "object",
                "x-de-$ref": "RefSchema",
                "description": "description 1",
            },
            id="description",
        ),
        pytest.param(
            types.ObjectArtifacts(
                spec={},
                logical_name="logical name 1",
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                write_only=True,
            ),
            {"type": "object", "x-de-$ref": "RefSchema", "writeOnly": True},
            id="writeOnly",
        ),
    ],
)
@pytest.mark.column
def test_calculate_schema(artifacts, expected_schema):
    """
    GIVEN object reference artifacts
    WHEN _calculate_schema is called with the artifacts
    THEN the calculate for the array reference is returned.
    """
    schema = object_ref._schema.calculate(artifacts=artifacts)

    assert schema == expected_schema
