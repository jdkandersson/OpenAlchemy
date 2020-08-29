"""Tests for types."""

import pytest

from open_alchemy import helpers as oa_helpers
from open_alchemy.schemas import artifacts
from open_alchemy.schemas import helpers


@pytest.mark.parametrize(
    "artifacts_value, expected_dict",
    [
        pytest.param(
            artifacts.types.OpenApiSimplePropertyArtifacts(
                type_="integer",
                format_=None,
                max_length=None,
                nullable=None,
                description=None,
                default=None,
                read_only=None,
                write_only=None,
            ),
            {"type": "integer"},
            id="open api opt values None",
        ),
        pytest.param(
            artifacts.types.OpenApiSimplePropertyArtifacts(
                type_="string",
                format_="format 1",
                max_length=11,
                nullable=True,
                description="description 1",
                default="default 1",
                read_only=False,
                write_only=True,
            ),
            {
                "type": "string",
                "format_": "format 1",
                "max_length": 11,
                "nullable": True,
                "description": "description 1",
                "default": "default 1",
                "read_only": False,
                "write_only": True,
            },
            id="open api opt values defined",
        ),
        pytest.param(
            artifacts.types.ExtensionSimplePropertyArtifacts(
                primary_key=True,
                autoincrement=None,
                index=None,
                unique=None,
                foreign_key=None,
                kwargs=None,
                foreign_key_kwargs=None,
            ),
            {"primary_key": True},
            id="extension opt values None",
        ),
        pytest.param(
            artifacts.types.ExtensionSimplePropertyArtifacts(
                primary_key=True,
                autoincrement=False,
                index=False,
                unique=True,
                foreign_key="foreign.key",
                kwargs={"key_1": "value 1"},
                foreign_key_kwargs={"key_2": "value 2"},
            ),
            {
                "primary_key": True,
                "autoincrement": False,
                "index": False,
                "unique": True,
                "foreign_key": "foreign.key",
                "kwargs": {"key_1": "value 1"},
                "foreign_key_kwargs": {"key_2": "value 2"},
            },
            id="extension opt values defined",
        ),
        pytest.param(
            artifacts.types.SimplePropertyArtifacts(
                type_=helpers.property_.type_.Type.SIMPLE,
                open_api=artifacts.types.OpenApiSimplePropertyArtifacts(
                    type_="integer",
                    format_=None,
                    max_length=None,
                    nullable=None,
                    description=None,
                    default=None,
                    read_only=None,
                    write_only=None,
                ),
                extension=artifacts.types.ExtensionSimplePropertyArtifacts(
                    primary_key=True,
                    autoincrement=None,
                    index=None,
                    unique=None,
                    foreign_key=None,
                    kwargs=None,
                    foreign_key_kwargs=None,
                ),
                schema={"type": "integer"},
                required=True,
            ),
            {
                "type": "SIMPLE",
                "open_api": {"type": "integer"},
                "extension": {"primary_key": True},
                "schema": {"type": "integer"},
                "required": True,
            },
            id="complete",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_simple_property_artifacts(artifacts_value, expected_dict):
    """
    GIVEN artifacts and expected dictionary
    WHEN to_dict is called on the artifacts
    THEN the expected dictionary is returned.
    """
    returned_dict = artifacts_value.to_dict()

    assert returned_dict == expected_dict


@pytest.mark.parametrize(
    "artifacts_value, expected_dict",
    [
        pytest.param(
            artifacts.types.OpenApiJsonPropertyArtifacts(
                nullable=None,
                description=None,
                read_only=None,
                write_only=None,
            ),
            {},
            id="open api opt values None",
        ),
        pytest.param(
            artifacts.types.OpenApiJsonPropertyArtifacts(
                nullable=True,
                description="description 1",
                read_only=False,
                write_only=True,
            ),
            {
                "nullable": True,
                "description": "description 1",
                "read_only": False,
                "write_only": True,
            },
            id="open api opt values defined",
        ),
        pytest.param(
            artifacts.types.ExtensionJsonPropertyArtifacts(
                primary_key=True,
                index=None,
                unique=None,
                foreign_key=None,
                kwargs=None,
                foreign_key_kwargs=None,
            ),
            {"primary_key": True},
            id="extension opt values None",
        ),
        pytest.param(
            artifacts.types.ExtensionJsonPropertyArtifacts(
                primary_key=True,
                index=False,
                unique=True,
                foreign_key="foreign.key",
                kwargs={"key_1": "value 1"},
                foreign_key_kwargs={"key_2": "value 2"},
            ),
            {
                "primary_key": True,
                "index": False,
                "unique": True,
                "foreign_key": "foreign.key",
                "kwargs": {"key_1": "value 1"},
                "foreign_key_kwargs": {"key_2": "value 2"},
            },
            id="extension opt values defined",
        ),
        pytest.param(
            artifacts.types.JsonPropertyArtifacts(
                type_=helpers.property_.type_.Type.JSON,
                open_api=artifacts.types.OpenApiJsonPropertyArtifacts(
                    nullable=True,
                    description=None,
                    read_only=None,
                    write_only=None,
                ),
                extension=artifacts.types.ExtensionJsonPropertyArtifacts(
                    primary_key=True,
                    index=None,
                    unique=None,
                    foreign_key=None,
                    kwargs=None,
                    foreign_key_kwargs=None,
                ),
                schema={"type": "integer"},
                required=True,
            ),
            {
                "type": "JSON",
                "open_api": {"nullable": True},
                "extension": {"primary_key": True},
                "schema": {"type": "integer"},
                "required": True,
            },
            id="complete",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_json_property_artifacts(artifacts_value, expected_dict):
    """
    GIVEN artifacts and expected dictionary
    WHEN to_dict is called on the artifacts
    THEN the expected dictionary is returned.
    """
    returned_dict = artifacts_value.to_dict()

    assert returned_dict == expected_dict


@pytest.mark.parametrize(
    "artifacts_value, expected_dict",
    [
        pytest.param(
            artifacts.types.OneToManyRelationshipPropertyArtifacts(
                type_=helpers.property_.type_.Type.RELATIONSHIP,
                schema={
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "parent"},
                },
                sub_type=oa_helpers.relationship.Type.ONE_TO_MANY,
                parent="parent 1",
                backref_property=None,
                kwargs=None,
                write_only=None,
                description=None,
                required=True,
                foreign_key="foreign.key",
                foreign_key_property="foreign_key",
            ),
            {
                "type": "RELATIONSHIP",
                "sub_type": "ONE_TO_MANY",
                "parent": "parent 1",
                "required": True,
                "foreign_key": "foreign.key",
                "foreign_key_property": "foreign_key",
                "schema": {
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "parent"},
                },
            },
            id="one-to-many relationship opt values not defined",
        ),
        pytest.param(
            artifacts.types.OneToManyRelationshipPropertyArtifacts(
                type_=helpers.property_.type_.Type.RELATIONSHIP,
                schema={
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "parent"},
                },
                sub_type=oa_helpers.relationship.Type.ONE_TO_MANY,
                parent="parent 1",
                backref_property="backref 1",
                kwargs={"key_": "value"},
                write_only=True,
                description="description 1",
                required=True,
                foreign_key="foreign.key",
                foreign_key_property="foreign_key",
            ),
            {
                "type": "RELATIONSHIP",
                "sub_type": "ONE_TO_MANY",
                "parent": "parent 1",
                "required": True,
                "backref_property": "backref 1",
                "kwargs": {"key_": "value"},
                "write_only": True,
                "description": "description 1",
                "foreign_key": "foreign.key",
                "foreign_key_property": "foreign_key",
                "schema": {
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "parent"},
                },
            },
            id="one-to-many relationship opt values defined",
        ),
        pytest.param(
            artifacts.types.ManyToOneRelationshipPropertyArtifacts(
                type_=helpers.property_.type_.Type.RELATIONSHIP,
                schema={"type": "object", "x-de-$ref": "parent"},
                sub_type=oa_helpers.relationship.Type.MANY_TO_ONE,
                parent="parent 1",
                backref_property=None,
                kwargs=None,
                write_only=None,
                description=None,
                required=True,
                foreign_key="foreign.key",
                foreign_key_property="foreign_key",
                nullable=None,
            ),
            {
                "type": "RELATIONSHIP",
                "sub_type": "MANY_TO_ONE",
                "parent": "parent 1",
                "required": True,
                "foreign_key": "foreign.key",
                "foreign_key_property": "foreign_key",
                "schema": {"type": "object", "x-de-$ref": "parent"},
            },
            id="many-to-one relationship opt values not defined",
        ),
        pytest.param(
            artifacts.types.ManyToOneRelationshipPropertyArtifacts(
                type_=helpers.property_.type_.Type.RELATIONSHIP,
                schema={"type": "object", "x-de-$ref": "parent"},
                sub_type=oa_helpers.relationship.Type.MANY_TO_ONE,
                parent="parent 1",
                backref_property="backref 1",
                kwargs={"key_": "value"},
                write_only=True,
                description="description 1",
                required=True,
                foreign_key="foreign.key",
                foreign_key_property="foreign_key",
                nullable=False,
            ),
            {
                "type": "RELATIONSHIP",
                "sub_type": "MANY_TO_ONE",
                "parent": "parent 1",
                "required": True,
                "backref_property": "backref 1",
                "kwargs": {"key_": "value"},
                "write_only": True,
                "description": "description 1",
                "foreign_key": "foreign.key",
                "foreign_key_property": "foreign_key",
                "schema": {"type": "object", "x-de-$ref": "parent"},
                "nullable": False,
            },
            id="many-to-one relationship opt values defined",
        ),
        pytest.param(
            artifacts.types.OneToOneRelationshipPropertyArtifacts(
                type_=helpers.property_.type_.Type.RELATIONSHIP,
                schema={"type": "object", "x-de-$ref": "parent"},
                sub_type=oa_helpers.relationship.Type.ONE_TO_ONE,
                parent="parent 1",
                backref_property=None,
                kwargs=None,
                write_only=None,
                description=None,
                required=True,
                foreign_key="foreign.key",
                foreign_key_property="foreign_key",
                nullable=None,
            ),
            {
                "type": "RELATIONSHIP",
                "sub_type": "ONE_TO_ONE",
                "parent": "parent 1",
                "required": True,
                "foreign_key": "foreign.key",
                "foreign_key_property": "foreign_key",
                "schema": {"type": "object", "x-de-$ref": "parent"},
            },
            id="one-to-one relationship opt values not defined",
        ),
        pytest.param(
            artifacts.types.OneToOneRelationshipPropertyArtifacts(
                type_=helpers.property_.type_.Type.RELATIONSHIP,
                schema={"type": "object", "x-de-$ref": "parent"},
                sub_type=oa_helpers.relationship.Type.ONE_TO_ONE,
                parent="parent 1",
                backref_property="backref 1",
                kwargs={"key_": "value"},
                write_only=True,
                description="description 1",
                required=True,
                foreign_key="foreign.key",
                foreign_key_property="foreign_key",
                nullable=False,
            ),
            {
                "type": "RELATIONSHIP",
                "sub_type": "ONE_TO_ONE",
                "parent": "parent 1",
                "required": True,
                "backref_property": "backref 1",
                "kwargs": {"key_": "value"},
                "write_only": True,
                "description": "description 1",
                "foreign_key": "foreign.key",
                "foreign_key_property": "foreign_key",
                "schema": {"type": "object", "x-de-$ref": "parent"},
                "nullable": False,
            },
            id="one-to-one relationship opt values defined",
        ),
        pytest.param(
            artifacts.types.ManyToManyRelationshipPropertyArtifacts(
                type_=helpers.property_.type_.Type.RELATIONSHIP,
                schema={
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "parent"},
                },
                sub_type=oa_helpers.relationship.Type.MANY_TO_MANY,
                parent="parent 1",
                backref_property=None,
                kwargs=None,
                write_only=None,
                description=None,
                required=True,
                secondary="secondary_1",
            ),
            {
                "type": "RELATIONSHIP",
                "sub_type": "MANY_TO_MANY",
                "parent": "parent 1",
                "required": True,
                "secondary": "secondary_1",
                "schema": {
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "parent"},
                },
            },
            id="one-to-many relationship opt values not defined",
        ),
        pytest.param(
            artifacts.types.ManyToManyRelationshipPropertyArtifacts(
                type_=helpers.property_.type_.Type.RELATIONSHIP,
                schema={
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "parent"},
                },
                sub_type=oa_helpers.relationship.Type.MANY_TO_MANY,
                parent="parent 1",
                backref_property="backref 1",
                kwargs={"key_": "value"},
                write_only=True,
                description="description 1",
                required=True,
                secondary="secondary_1",
            ),
            {
                "type": "RELATIONSHIP",
                "sub_type": "MANY_TO_MANY",
                "parent": "parent 1",
                "required": True,
                "backref_property": "backref 1",
                "kwargs": {"key_": "value"},
                "write_only": True,
                "description": "description 1",
                "secondary": "secondary_1",
                "schema": {
                    "type": "array",
                    "items": {"type": "object", "x-de-$ref": "parent"},
                },
            },
            id="one-to-many relationship opt values defined",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_relationship_property_artifacts(artifacts_value, expected_dict):
    """
    GIVEN artifacts and expected dictionary
    WHEN to_dict is called on the artifacts
    THEN the expected dictionary is returned.
    """
    returned_dict = artifacts_value.to_dict()

    assert returned_dict == expected_dict


@pytest.mark.parametrize(
    "artifacts_value, expected_dict",
    [
        pytest.param(
            artifacts.types.BackrefPropertyArtifacts(
                type_=helpers.property_.type_.Type.BACKREF,
                sub_type=artifacts.types.BackrefSubType.OBJECT,
                schema={"type": "object"},
                properties=["property_1"],
                required=None,
            ),
            {
                "type": "BACKREF",
                "sub_type": "OBJECT",
                "schema": {"type": "object"},
                "properties": ["property_1"],
            },
            id="object",
        ),
        pytest.param(
            artifacts.types.BackrefPropertyArtifacts(
                type_=helpers.property_.type_.Type.BACKREF,
                sub_type=artifacts.types.BackrefSubType.ARRAY,
                schema={"type": "object"},
                properties=["property_1"],
                required=None,
            ),
            {
                "type": "BACKREF",
                "sub_type": "ARRAY",
                "schema": {"type": "object"},
                "properties": ["property_1"],
            },
            id="object",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.artifacts
def test_backref_property_artifacts(artifacts_value, expected_dict):
    """
    GIVEN artifacts and expected dictionary
    WHEN to_dict is called on the artifacts
    THEN the expected dictionary is returned.
    """
    returned_dict = artifacts_value.to_dict()

    assert returned_dict == expected_dict


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
