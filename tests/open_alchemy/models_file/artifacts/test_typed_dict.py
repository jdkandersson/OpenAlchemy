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
            nullable=False,
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
        nullable=False,
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
        nullable=False,
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


def _construct_backref_property_artifacts(sub_type):
    """Construct backref property artifacts."""
    return schemas_artifacts.types.BackrefPropertyArtifacts(
        type=helpers.property_.type_.Type.BACKREF,
        sub_type=sub_type,
        schema={},  # type: ignore
        properties=[],
        required=None,
        description=None,
    )


CALCULATE_TESTS = [
    pytest.param([], [], id="empty"),
    pytest.param(
        [
            (
                "prop_1",
                _construct_backref_property_artifacts(
                    schemas_artifacts.types.BackrefSubType.OBJECT
                ),
            )
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type=(
                    "typing.Optional[typing.Dict["
                    "str, typing.Union[int, float, str, bool]]]"
                ),
                description=None,
            ),
        ],
        id="single backref object",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_backref_property_artifacts(
                    schemas_artifacts.types.BackrefSubType.ARRAY
                ),
            )
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type=(
                    "typing.Sequence[typing.Dict["
                    "str, typing.Union[int, float, str, bool]]]"
                ),
                description=None,
            ),
        ],
        id="single backref array",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    dict_ignore=True, description=None
                ),
            )
        ],
        [],
        id="single dict ignore",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    dict_ignore=False, description=None
                ),
            )
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="int",
                description=None,
            ),
        ],
        id="single simple",
    ),
    pytest.param(
        [("prop_1", _construct_json_property_artifacts())],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="typing.Any",
                description=None,
            )
        ],
        id="single json",
    ),
    pytest.param(
        [("prop_1", _construct_many_to_one_relationship_property_artifacts())],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='"RefModelDict"',
                description=None,
            )
        ],
        id="single relationship many-to-one",
    ),
    pytest.param(
        [("prop_1", _construct_one_to_one_relationship_property_artifacts())],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='"RefModelDict"',
                description=None,
            )
        ],
        id="single relationship one-to-one",
    ),
    pytest.param(
        [("prop_1", _construct_one_to_many_relationship_property_artifacts())],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='typing.Sequence["RefModelDict"]',
                description=None,
            )
        ],
        id="single relationship one-to-many",
    ),
    pytest.param(
        [("prop_1", _construct_many_to_many_relationship_property_artifacts())],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='typing.Sequence["RefModelDict"]',
                description=None,
            )
        ],
        id="single relationship many-to-many",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    dict_ignore=False, description="description 1"
                ),
            )
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="int",
                description="description 1",
            )
        ],
        id="single description",
    ),
    pytest.param(
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
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="int",
                description=None,
            ),
            models_file.types.ColumnArtifacts(
                name="prop_2",
                type="int",
                description=None,
            ),
        ],
        id="multiple",
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
    returned_columns = models_file.artifacts._typed_dict._calculate(artifacts=artifacts)

    assert list(returned_columns) == expected_columns
