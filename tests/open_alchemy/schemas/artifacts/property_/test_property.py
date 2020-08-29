"""Tests for retrieving artifacts for a property."""

import functools

import pytest

from open_alchemy.schemas import artifacts
from open_alchemy.schemas.helpers.property_ import type_

GET_TESTS = [
    pytest.param(
        True,
        {"type": "integer"},
        {},
        "required",
        True,
        artifacts.types.SimplePropertyArtifacts,
        id="simple required True",
    ),
    pytest.param(
        False,
        {"type": "integer"},
        {},
        "required",
        False,
        artifacts.types.SimplePropertyArtifacts,
        id="simple required False",
    ),
    pytest.param(
        None,
        {"type": "integer"},
        {},
        "type",
        type_.Type.SIMPLE,
        artifacts.types.SimplePropertyArtifacts,
        id="simple type_",
    ),
    pytest.param(
        True,
        {"x-json": True},
        {},
        "required",
        True,
        artifacts.types.JsonPropertyArtifacts,
        id="JSON required True",
    ),
    pytest.param(
        False,
        {"x-json": True},
        {},
        "required",
        False,
        artifacts.types.JsonPropertyArtifacts,
        id="JSON required False",
    ),
    pytest.param(
        None,
        {"x-json": True},
        {},
        "type",
        type_.Type.JSON,
        artifacts.types.JsonPropertyArtifacts,
        id="JSON type_",
    ),
    pytest.param(
        None,
        {"readOnly": True, "type": "object"},
        {},
        "type",
        type_.Type.BACKREF,
        artifacts.types.BackrefPropertyArtifacts,
        id="backref type_",
    ),
    pytest.param(
        True,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        "required",
        True,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="required True",
    ),
    pytest.param(
        False,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        "required",
        False,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="required False",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        "type",
        type_.Type.RELATIONSHIP,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="property type",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        "foreign_key_property",
        "property_1_id",
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="foreign key property many-to-one",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
        "foreign_key_property",
        "schema_property_1_id",
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="foreign key property one-to-many",
    ),
]


@pytest.mark.parametrize(
    "required, schema, schemas, key, expected_value, expected_type", GET_TESTS
)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_get(required, schema, schemas, key, expected_value, expected_type):
    """
    GIVEN schema, schemas, key and expected value
    WHEN get is called with the schema, property name, parent schema and schemas
    THEN the returned artifacts has the expected value behind the key.
    """
    parent_schema = {"x-tablename": "schema"}
    property_name = "property_1"

    returned_artifacts = artifacts.property_.get(
        schemas, parent_schema, property_name, schema, required
    )

    assert isinstance(returned_artifacts, expected_type)
    value = functools.reduce(getattr, key.split("."), returned_artifacts)
    assert value == expected_value
