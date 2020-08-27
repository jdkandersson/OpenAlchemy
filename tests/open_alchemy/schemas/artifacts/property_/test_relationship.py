"""Tests for retrieving artifacts for a relationship property."""

import functools

import pytest

from open_alchemy import helpers
from open_alchemy.schemas import artifacts
from open_alchemy.schemas.helpers.property_ import type_

GET_TESTS = [
    pytest.param(
        True,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "required",
        True,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="required True",
    ),
    pytest.param(
        False,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "required",
        False,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="required False",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "type_",
        type_.Type.RELATIONSHIP,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="property type",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "sub_type",
        helpers.relationship.Type.MANY_TO_ONE,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="sub type many-to-one",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-uselist": False}},
        "sub_type",
        helpers.relationship.Type.ONE_TO_ONE,
        artifacts.types.OneToOneRelationshipPropertyArtifacts,
        id="sub type one-to-one",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object"}},
        "sub_type",
        helpers.relationship.Type.ONE_TO_MANY,
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="sub type one-to-many",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-secondary": "secondary_1"}},
        "sub_type",
        helpers.relationship.Type.MANY_TO_MANY,
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="sub type many-to-many",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "parent",
        "RefSchema",
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="parent many-to-one",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-uselist": False}},
        "parent",
        "RefSchema",
        artifacts.types.OneToOneRelationshipPropertyArtifacts,
        id="parent one-to-one",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object"}},
        "parent",
        "RefSchema",
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="parent one-to-many",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-secondary": "secondary_1"}},
        "parent",
        "RefSchema",
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="parent many-to-many",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/RefRefSchema"},
            },
            "RefRefSchema": {"type": "object"},
        },
        "parent",
        "RefRefSchema",
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="$ref items one-to-many",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
            ]
        },
        {"RefSchema": {"type": "object"}},
        "parent",
        "RefSchema",
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="allOf items one-to-many",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/RefRefSchema"},
            },
            "RefRefSchema": {"type": "object", "x-secondary": "secondary_1"},
        },
        "parent",
        "RefRefSchema",
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="$ref items one-to-many",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
            ]
        },
        {"RefSchema": {"type": "object", "x-secondary": "secondary_1"}},
        "parent",
        "RefSchema",
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="allOf items one-to-many",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "schema",
        {"type": "object", "x-de-$ref": "RefSchema"},
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="schema many-to-one",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"description": "description 1"},
            ]
        },
        {"RefSchema": {"type": "object", "description": "description 2"}},
        "schema",
        {"type": "object", "x-de-$ref": "RefSchema", "description": "description 1"},
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="schema description prefer local many-to-one",
    ),
    pytest.param(
        None,
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"nullable": True}]},
        {"RefSchema": {"type": "object", "nullable": False}},
        "schema",
        {"type": "object", "x-de-$ref": "RefSchema", "nullable": True},
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="schema nullable prefer local many-to-one",
    ),
    pytest.param(
        None,
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"writeOnly": True}]},
        {"RefSchema": {"type": "object", "writeOnly": False}},
        "schema",
        {"type": "object", "x-de-$ref": "RefSchema", "writeOnly": True},
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="schema writeOnly prefer local many-to-one",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-uselist": False}},
        "schema",
        {"type": "object", "x-de-$ref": "RefSchema"},
        artifacts.types.OneToOneRelationshipPropertyArtifacts,
        id="schema one-to-one",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object"}},
        "schema",
        {"type": "array", "items": {"type": "object", "x-de-$ref": "RefSchema"}},
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="schema one-to-many",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
                {"description": "description 1"},
            ]
        },
        {"RefSchema": {"type": "object", "description": "description 2"}},
        "schema",
        {
            "type": "array",
            "items": {"type": "object", "x-de-$ref": "RefSchema"},
            "description": "description 1",
        },
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="schema description one-to-many",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
                {"writeOnly": True},
            ]
        },
        {"RefSchema": {"type": "object", "writeOnly": False}},
        "schema",
        {
            "type": "array",
            "items": {"type": "object", "x-de-$ref": "RefSchema"},
            "writeOnly": True,
        },
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="schema writeOnly one-to-many",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-secondary": "secondary_1"}},
        "schema",
        {"type": "array", "items": {"type": "object", "x-de-$ref": "RefSchema"}},
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="schema many-to-many",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "backref_property",
        None,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="backref undefined",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-backref": "backref_1"},
            ]
        },
        {"RefSchema": {"type": "object"}},
        "backref_property",
        "backref_1",
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="backref many-to-one",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-backref": "backref_1"},
            ]
        },
        {"RefSchema": {"type": "object", "x-backref": "backref_2"}},
        "backref_property",
        "backref_1",
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="backref prefer local many-to-one",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-backref": "backref_1", "x-uselist": False}},
        "backref_property",
        "backref_1",
        artifacts.types.OneToOneRelationshipPropertyArtifacts,
        id="backref one-to-one",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-backref": "backref_1"}},
        "backref_property",
        "backref_1",
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="backref one-to-many",
    ),
    pytest.param(
        None,
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "type": "object",
                "x-backref": "backref_1",
                "x-secondary": "secondary_1",
            }
        },
        "backref_property",
        "backref_1",
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="backref many-to-many",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "kwargs",
        None,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="kwargs undefined",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-kwargs": {"key_1": "value 1"}},
            ]
        },
        {"RefSchema": {"type": "object"}},
        "kwargs",
        {"key_1": "value 1"},
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="kwargs many-to-one",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-kwargs": {"key_2": "value 2"}}},
        "kwargs",
        None,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="kwargs on parent many-to-one",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-kwargs": {"key_1": "value 1"}},
            ]
        },
        {"RefSchema": {"type": "object", "x-uselist": False}},
        "kwargs",
        {"key_1": "value 1"},
        artifacts.types.OneToOneRelationshipPropertyArtifacts,
        id="kwargs one-to-one",
    ),
    pytest.param(
        None,
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"key_1": "value 1"}},
                ]
            },
        },
        {"RefSchema": {"type": "object"}},
        "kwargs",
        {"key_1": "value 1"},
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="kwargs one-to-many",
    ),
    pytest.param(
        None,
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-kwargs": {"key_1": "value 1"}},
                ]
            },
        },
        {"RefSchema": {"type": "object", "x-secondary": "secondary_1",}},
        "kwargs",
        {"key_1": "value 1"},
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="kwargs many-to-many",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "write_only",
        None,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="writeOnly undefined",
    ),
    pytest.param(
        None,
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"writeOnly": True}]},
        {"RefSchema": {"type": "object"}},
        "write_only",
        True,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="writeOnly many-to-one",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "writeOnly": True}},
        "write_only",
        None,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="writeOnly many-to-one skip_ref",
    ),
    pytest.param(
        None,
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"writeOnly": False}]},
        {"RefSchema": {"type": "object", "x-uselist": False}},
        "write_only",
        False,
        artifacts.types.OneToOneRelationshipPropertyArtifacts,
        id="writeOnly one-to-one",
    ),
    pytest.param(
        None,
        {
            "writeOnly": True,
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object"}},
        "write_only",
        True,
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="writeOnly one-to-many",
    ),
    pytest.param(
        None,
        {
            "writeOnly": True,
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-secondary": "secondary_1"}},
        "write_only",
        True,
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="writeOnly many-to-many",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        "description",
        None,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="description undefined",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"description": "description 1"},
            ]
        },
        {"RefSchema": {"type": "object"}},
        "description",
        "description 1",
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="description many-to-one",
    ),
    pytest.param(
        None,
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "description": "description 1"}},
        "description",
        None,
        artifacts.types.ManyToOneRelationshipPropertyArtifacts,
        id="description many-to-one skip_ref",
    ),
    pytest.param(
        None,
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"description": "description 2"},
            ]
        },
        {"RefSchema": {"type": "object", "x-uselist": False}},
        "description",
        "description 2",
        artifacts.types.OneToOneRelationshipPropertyArtifacts,
        id="description one-to-one",
    ),
    pytest.param(
        None,
        {
            "description": "description 1",
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object"}},
        "description",
        "description 1",
        artifacts.types.OneToManyRelationshipPropertyArtifacts,
        id="description one-to-many",
    ),
    pytest.param(
        None,
        {
            "description": "description 1",
            "type": "array",
            "items": {"$ref": "#/components/schemas/RefSchema"},
        },
        {"RefSchema": {"type": "object", "x-secondary": "secondary_1"}},
        "description",
        "description 1",
        artifacts.types.ManyToManyRelationshipPropertyArtifacts,
        id="description many-to-many",
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
    WHEN get is called with the schema and schemas
    THEN the returned artifacts has the expected value behind the key.
    """
    returned_artifacts = artifacts.property_.relationship.get(schemas, schema, required)

    assert isinstance(returned_artifacts, expected_type)
    value = functools.reduce(getattr, key.split("."), returned_artifacts)
    assert value == expected_value
