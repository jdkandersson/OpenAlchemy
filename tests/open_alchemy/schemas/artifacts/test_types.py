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
                type="integer",
                format=None,
                max_length=None,
                nullable=None,
                default=None,
                read_only=None,
                write_only=None,
            ),
            {"type": "integer"},
            id="open api opt values None",
        ),
        pytest.param(
            artifacts.types.OpenApiSimplePropertyArtifacts(
                type="string",
                format="format 1",
                max_length=11,
                nullable=True,
                default="default 1",
                read_only=False,
                write_only=True,
            ),
            {
                "type": "string",
                "format": "format 1",
                "max_length": 11,
                "nullable": True,
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
                dict_ignore=None,
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
                dict_ignore=True,
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
                type=helpers.property_.type_.Type.SIMPLE,
                description=None,
                open_api=artifacts.types.OpenApiSimplePropertyArtifacts(
                    type="integer",
                    format=None,
                    max_length=None,
                    nullable=None,
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
                    dict_ignore=None,
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
            id="complete optional not defined",
        ),
        pytest.param(
            artifacts.types.SimplePropertyArtifacts(
                type=helpers.property_.type_.Type.SIMPLE,
                description="description 1",
                open_api=artifacts.types.OpenApiSimplePropertyArtifacts(
                    type="integer",
                    format=None,
                    max_length=None,
                    nullable=None,
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
                    dict_ignore=None,
                ),
                schema={"type": "integer"},
                required=True,
            ),
            {
                "type": "SIMPLE",
                "description": "description 1",
                "open_api": {"type": "integer"},
                "extension": {"primary_key": True},
                "schema": {"type": "integer"},
                "required": True,
            },
            id="complete optional defined",
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
                read_only=None,
                write_only=None,
            ),
            {},
            id="open api opt values None",
        ),
        pytest.param(
            artifacts.types.OpenApiJsonPropertyArtifacts(
                nullable=True,
                read_only=False,
                write_only=True,
            ),
            {
                "nullable": True,
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
                description=None,
                type=helpers.property_.type_.Type.JSON,
                open_api=artifacts.types.OpenApiJsonPropertyArtifacts(
                    nullable=True,
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
            id="complete opt values not defined",
        ),
        pytest.param(
            artifacts.types.JsonPropertyArtifacts(
                description="description 1",
                type=helpers.property_.type_.Type.JSON,
                open_api=artifacts.types.OpenApiJsonPropertyArtifacts(
                    nullable=True,
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
                "description": "description 1",
                "open_api": {"nullable": True},
                "extension": {"primary_key": True},
                "schema": {"type": "integer"},
                "required": True,
            },
            id="complete opt values defined",
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
                type=helpers.property_.type_.Type.RELATIONSHIP,
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
                type=helpers.property_.type_.Type.RELATIONSHIP,
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
                type=helpers.property_.type_.Type.RELATIONSHIP,
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
                type=helpers.property_.type_.Type.RELATIONSHIP,
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
                type=helpers.property_.type_.Type.RELATIONSHIP,
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
                type=helpers.property_.type_.Type.RELATIONSHIP,
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
                type=helpers.property_.type_.Type.RELATIONSHIP,
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
                type=helpers.property_.type_.Type.RELATIONSHIP,
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
                type=helpers.property_.type_.Type.BACKREF,
                sub_type=artifacts.types.BackrefSubType.OBJECT,
                description=None,
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
                type=helpers.property_.type_.Type.BACKREF,
                sub_type=artifacts.types.BackrefSubType.ARRAY,
                description="description 1",
                schema={"type": "array"},
                properties=["property_1"],
                required=None,
            ),
            {
                "type": "BACKREF",
                "description": "description 1",
                "sub_type": "ARRAY",
                "schema": {"type": "array"},
                "properties": ["property_1"],
            },
            id="array",
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
            artifacts.types.ModelExPropertiesArtifacts(
                tablename="table_1",
                inherits=None,
                parent=None,
                description=None,
                mixins=None,
                kwargs=None,
                composite_index=None,
                composite_unique=None,
                backrefs=[],
            ),
            {"tablename": "table_1"},
            id="opt values None",
        ),
        pytest.param(
            artifacts.types.ModelExPropertiesArtifacts(
                tablename="table_1",
                inherits=True,
                parent="Parent1",
                description="description 1",
                mixins=["model.Mixin1"],
                kwargs={"key": "value"},
                composite_index=[{"expressions": ["column_1"]}],
                composite_unique=[{"columns": ["column_1"]}],
                backrefs=[],
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
