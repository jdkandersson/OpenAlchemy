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


def _construct_simple_property_artifacts(
    dict_ignore, description, write_only, required
):
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
            write_only=write_only,
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
        required=required,
        description=description,
    )


def _construct_json_property_artifacts(write_only):
    """Construct the artifacts for a json property."""
    return schemas_artifacts.types.JsonPropertyArtifacts(
        type=helpers.property_.type_.Type.JSON,
        open_api=schemas_artifacts.types.OpenApiJsonPropertyArtifacts(
            nullable=False,
            read_only=None,
            write_only=write_only,
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


def _construct_many_to_one_relationship_property_artifacts(write_only):
    """Construct many-to-one relationship property artifacts."""
    return schemas_artifacts.types.ManyToOneRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.MANY_TO_ONE,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=write_only,
        description=None,
        required=False,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=False,
    )


def _construct_one_to_one_relationship_property_artifacts(write_only):
    """Construct one-to-one relationship property artifacts."""
    return schemas_artifacts.types.OneToOneRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.ONE_TO_ONE,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=write_only,
        description=None,
        required=False,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=False,
    )


def _construct_one_to_many_relationship_property_artifacts(write_only):
    """Construct one-to-many relationship property artifacts."""
    return schemas_artifacts.types.OneToManyRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.ONE_TO_MANY,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=write_only,
        description=None,
        required=False,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
    )


def _construct_many_to_many_relationship_property_artifacts(write_only):
    """Construct many-to-many relationship artifacts."""
    return schemas_artifacts.types.ManyToManyRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.MANY_TO_MANY,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=write_only,
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


def _construct_backrefs_item():
    """Construct a model backref item."""
    return schemas_artifacts.types.ModelBackrefArtifacts(
        type=schemas_artifacts.types.BackrefSubType.OBJECT,
        child="Child1",
    )


_CALCULATE_TESTS = [
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
                    dict_ignore=True, description=None, write_only=False, required=False
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
                    dict_ignore=False, description=None, write_only=None, required=False
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
        id="single simple write only None",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    dict_ignore=False,
                    description=None,
                    write_only=False,
                    required=False,
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
        id="single simple write only False",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    dict_ignore=False, description=None, write_only=True, required=False
                ),
            )
        ],
        [],
        id="single simple write only True",
    ),
    pytest.param(
        [("prop_1", _construct_json_property_artifacts(write_only=None))],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="typing.Any",
                description=None,
            )
        ],
        id="single json write only None",
    ),
    pytest.param(
        [("prop_1", _construct_json_property_artifacts(write_only=False))],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="typing.Any",
                description=None,
            )
        ],
        id="single json write only False",
    ),
    pytest.param(
        [("prop_1", _construct_json_property_artifacts(write_only=True))],
        [],
        id="single json write only True",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_many_to_one_relationship_property_artifacts(write_only=None),
            )
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='"RefModelDict"',
                description=None,
            )
        ],
        id="single relationship many-to-one write only None",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_many_to_one_relationship_property_artifacts(
                    write_only=False
                ),
            )
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='"RefModelDict"',
                description=None,
            )
        ],
        id="single relationship many-to-one write only False",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_many_to_one_relationship_property_artifacts(write_only=True),
            )
        ],
        [],
        id="single relationship many-to-one write only True",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_one_to_one_relationship_property_artifacts(write_only=None),
            )
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type='"RefModelDict"',
                description=None,
            )
        ],
        id="single relationship one-to-one write only None",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_one_to_many_relationship_property_artifacts(write_only=None),
            )
        ],
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
        [
            (
                "prop_1",
                _construct_many_to_many_relationship_property_artifacts(
                    write_only=None
                ),
            )
        ],
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
                    dict_ignore=False,
                    description="description 1",
                    write_only=None,
                    required=False,
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
                    dict_ignore=False, description=None, write_only=None, required=False
                ),
            ),
            (
                "prop_2",
                _construct_simple_property_artifacts(
                    dict_ignore=False, description=None, write_only=None, required=False
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


@pytest.mark.parametrize("artifacts, expected_columns", _CALCULATE_TESTS)
@pytest.mark.models_file
@pytest.mark.artifacts
def test__calculate(artifacts, expected_columns):
    """
    GIVEN artifacts and expected columns
    WHEN _calculate is called with the artifacts
    THEN the expected columns are returned.
    """
    returned_columns = models_file.artifacts._typed_dict._calculate(artifacts=artifacts)

    assert list(returned_columns) == expected_columns


CALCULATE_TESTS = [
    pytest.param(_construct_model_artifacts([], []), [], [], id="empty"),
    pytest.param(
        _construct_model_artifacts([], [("backref_1", _construct_backrefs_item())]),
        [],
        [],
        id="single backrefs",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=True,
                    ),
                )
            ],
            [],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="int",
                description=None,
            ),
        ],
        [],
        id="single required",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=False,
                    ),
                )
            ],
            [],
        ),
        [],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="int",
                description=None,
            ),
        ],
        id="single not required",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=True,
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=True,
                    ),
                ),
            ],
            [],
        ),
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
        [],
        id="multiple required",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=False,
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=True,
                    ),
                ),
            ],
            [],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_2",
                type="int",
                description=None,
            ),
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="int",
                description=None,
            ),
        ],
        id="multiple first not required",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=True,
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=False,
                    ),
                ),
            ],
            [],
        ),
        [
            models_file.types.ColumnArtifacts(
                name="prop_1",
                type="int",
                description=None,
            ),
        ],
        [
            models_file.types.ColumnArtifacts(
                name="prop_2",
                type="int",
                description=None,
            ),
        ],
        id="multiple last not required",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=False,
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        dict_ignore=False,
                        description=None,
                        write_only=None,
                        required=False,
                    ),
                ),
            ],
            [],
        ),
        [],
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
        id="multiple not required",
    ),
]


@pytest.mark.parametrize(
    "artifacts, expected_required_columns, expected_not_required_columns",
    CALCULATE_TESTS,
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate(artifacts, expected_required_columns, expected_not_required_columns):
    """
    GIVEN artifacts and expected required and not required columns
    WHEN calculate is called with the artifacts
    THEN the expected columns are returned.
    """
    returned_columns = models_file.artifacts._typed_dict.calculate(artifacts=artifacts)

    assert returned_columns.required == expected_required_columns
    assert returned_columns.not_required == expected_not_required_columns
