"""Tests for calculating column artifacts."""

# pylint: disable=protected-access

import pytest

from open_alchemy import helpers as oa_helpers
from open_alchemy import models_file
from open_alchemy.schemas import artifacts as schemas_artifacts
from open_alchemy.schemas import helpers


def _construct_model_artifacts(properties, backrefs):
    """Construct model artifacts"""
    return schemas_artifacts.types.ModelArtifacts(
        tablename="table 1",
        inherits=None,
        parent=None,
        description=None,
        mixins=None,
        kwargs=None,
        composite_index=None,
        composite_unique=None,
        backrefs=backrefs,
        properties=properties,
    )


def _construct_simple_property_artifacts(dict_ignore, description):
    """Construct the artifacts for a simple property."""
    return schemas_artifacts.types.SimplePropertyArtifacts(
        type=helpers.property_.type_.Type.SIMPLE,
        open_api=schemas_artifacts.types.OpenApiSimplePropertyArtifacts(
            type="integer",
            format=None,
            max_length=None,
            nullable=None,
            default=None,
            read_only=None,
            write_only=None,
        ),
        extension=schemas_artifacts.types.ExtensionSimplePropertyArtifacts(
            primary_key=False,
            autoincrement=None,
            index=None,
            unique=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
            dict_ignore=dict_ignore,
        ),
        schema={},  # type: ignore
        required=False,
        description=description,
    )


def _construct_json_property_artifacts():
    """Construct the artifacts for a json property."""
    return schemas_artifacts.types.JsonPropertyArtifacts(
        type=helpers.property_.type_.Type.JSON,
        open_api=schemas_artifacts.types.OpenApiJsonPropertyArtifacts(
            nullable=False,
            read_only=None,
            write_only=None,
        ),
        extension=schemas_artifacts.types.ExtensionJsonPropertyArtifacts(
            primary_key=False,
            index=None,
            unique=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
        ),
        schema={},  # type: ignore
        required=False,
        description=None,
    )


def _construct_many_to_one_relationship_property_artifacts():
    """Construct many-to-one relationship property artifacts."""
    return schemas_artifacts.types.ManyToOneRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.MANY_TO_ONE,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=False,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=None,
    )


def _construct_one_to_one_relationship_property_artifacts():
    """Construct one-to-one relationship property artifacts."""
    return schemas_artifacts.types.OneToOneRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.ONE_TO_ONE,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=False,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=None,
    )


def _construct_one_to_many_relationship_property_artifacts():
    """Construct one-to-many relationship property artifacts."""
    return schemas_artifacts.types.OneToManyRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.ONE_TO_MANY,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=False,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
    )


def _construct_many_to_many_relationship_property_artifacts():
    """Construct many-to-many relationship artifacts."""
    return schemas_artifacts.types.ManyToManyRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.MANY_TO_MANY,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=False,
        secondary="secondary_1",
    )


def _construct_backref_property_artifacts():
    """Construct backref property artifacts."""
    return schemas_artifacts.types.BackrefPropertyArtifacts(
        type=helpers.property_.type_.Type.BACKREF,
        sub_type=schemas_artifacts.types.BackrefSubType.OBJECT,
        schema={},  # type: ignore
        properties=[],
        required=None,
        description=None,
    )


def _construct_backrefs_item(type_, child):
    """Construct a model backref item."""
    return schemas_artifacts.types.ModelBackrefArtifacts(
        type=type_,
        child=child,
    )


CALCULATE_TESTS = [
    pytest.param(
        _construct_model_artifacts([], []), [], id="empty properties and backreferences"
    ),
    pytest.param(
        _construct_model_artifacts(
            [("prop_1", _construct_backref_property_artifacts())], []
        ),
        [],
        id="single properties backref",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=True, description=None
                    ),
                )
            ],
            [],
        ),
        [],
        id="single properties dict ignore",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False, description=None
                    ),
                )
            ],
            [],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="typing.Optional[int]",
                description=None,
            )
        ],
        id="single properties simple",
    ),
    pytest.param(
        _construct_model_artifacts(
            [("prop_1", _construct_json_property_artifacts())], []
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="typing.Any",
                description=None,
            )
        ],
        id="single properties json",
    ),
    pytest.param(
        _construct_model_artifacts(
            [("prop_1", _construct_many_to_one_relationship_property_artifacts())], []
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='typing.Optional["TRefModel"]',
                description=None,
            )
        ],
        id="single properties relationship many-to-one",
    ),
    pytest.param(
        _construct_model_artifacts(
            [("prop_1", _construct_one_to_one_relationship_property_artifacts())], []
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='typing.Optional["TRefModel"]',
                description=None,
            )
        ],
        id="single properties relationship one-to-one",
    ),
    pytest.param(
        _construct_model_artifacts(
            [("prop_1", _construct_one_to_many_relationship_property_artifacts())], []
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='typing.Sequence["TRefModel"]',
                description=None,
            )
        ],
        id="single properties relationship one-to-many",
    ),
    pytest.param(
        _construct_model_artifacts(
            [("prop_1", _construct_many_to_many_relationship_property_artifacts())], []
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='typing.Sequence["TRefModel"]',
                description=None,
            )
        ],
        id="single properties relationship many-to-many",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False, description="description 1"
                    ),
                )
            ],
            [],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="typing.Optional[int]",
                description="description 1",
            )
        ],
        id="single properties description",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False, description=None
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        dict_ignore=False, description=None
                    ),
                ),
            ],
            [],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="typing.Optional[int]",
                description=None,
            ),
            models_file.types.ColumnArtifacts(
                name="prop_2",
                type="typing.Optional[int]",
                description=None,
            ),
        ],
        id="multiple properties",
    ),
    pytest.param(
        _construct_model_artifacts(
            [],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        schemas_artifacts.types.BackrefSubType.OBJECT, "Parent1"
                    ),
                )
            ],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="backref_1",
                type='typing.Optional["TParent1"]',
                description=None,
            ),
        ],
        id="single backreferences object",
    ),
    pytest.param(
        _construct_model_artifacts(
            [],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        schemas_artifacts.types.BackrefSubType.ARRAY, "Child1"
                    ),
                )
            ],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="backref_1",
                type='typing.Sequence["TChild1"]',
                description=None,
            ),
        ],
        id="single backreferences array",
    ),
    pytest.param(
        _construct_model_artifacts(
            [],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        schemas_artifacts.types.BackrefSubType.OBJECT, "Child1"
                    ),
                ),
                (
                    "backref_2",
                    _construct_backrefs_item(
                        schemas_artifacts.types.BackrefSubType.OBJECT, "Child2"
                    ),
                ),
            ],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="backref_1",
                type='typing.Optional["TChild1"]',
                description=None,
            ),
            models_file.types.ColumnArtifacts(
                name="backref_2",
                type='typing.Optional["TChild2"]',
                description=None,
            ),
        ],
        id="multiple backreferences",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False, description=None
                    ),
                )
            ],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        schemas_artifacts.types.BackrefSubType.ARRAY, "Child1"
                    ),
                )
            ],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="typing.Optional[int]",
                description=None,
            ),
            models_file.types.ColumnArtifacts(
                name="backref_1",
                type='typing.Sequence["TChild1"]',
                description=None,
            ),
        ],
        id="single properties and backreferences",
    ),
]


@pytest.mark.parametrize("artifacts, expected_columns", CALCULATE_TESTS)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate(artifacts, expected_columns):
    """
    GIVEN artifacts and expected columns
    WHEN calculate is called with the artifacts
    THEN the expected columns are returned.
    """
    returned_columns = models_file.artifacts._column.calculate(artifacts=artifacts)

    assert returned_columns == expected_columns
