"""Tests for artifacts"""

# pylint: disable=protected-access

import sys

import pytest

from open_alchemy import models_file
from open_alchemy.schemas import artifacts as schemas_artifacts
from open_alchemy.schemas import helpers


def _construct_model_artifacts(properties, description):
    """Construct model artifacts"""
    return schemas_artifacts.types.ModelArtifacts(
        tablename="table 1",
        inherits=None,
        parent=None,
        description=description,
        mixins=None,
        kwargs=None,
        composite_index=None,
        composite_unique=None,
        backrefs=[],
        properties=properties,
    )


def _construct_simple_property_artifacts(required):
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
            dict_ignore=None,
        ),
        schema={},  # type: ignore
        required=required,
        description=None,
    )


@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_name():
    """
    GIVEN name
    WHEN calculate is called with the name
    THEN the name is added to the artifacts.
    """
    artifacts = _construct_model_artifacts([], None)
    name = "Model"

    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name=name
    )

    assert returned_artifacts.sqlalchemy.name == name


@pytest.mark.parametrize(
    "artifacts, expected_description",
    [
        pytest.param(_construct_model_artifacts([], None), None, id="missing"),
        pytest.param(
            _construct_model_artifacts([], "description 1"), "description 1", id="set"
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_description(artifacts, expected_description):
    """
    GIVEN artifacts
    WHEN calculate is called with the artifacts
    THEN the description is added to the artifacts.
    """
    name = "Model"

    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name=name
    )

    assert returned_artifacts.sqlalchemy.description == expected_description


_EXPECTED_CLS_BASE = "typing.Protocol"
if sys.version_info[1] < 8:
    _EXPECTED_CLS_BASE = "typing_extensions.Protocol"


@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_parent():
    """
    GIVEN
    WHEN calculate is called
    THEN the correct parent class is set.
    """
    artifacts = _construct_model_artifacts([], None)

    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name="Model"
    )

    assert returned_artifacts.sqlalchemy.parent_cls == _EXPECTED_CLS_BASE


@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_column():
    """
    GIVEN artifacts
    WHEN calculate is called with the artifacts
    THEN the given expected columns are added to the artifacts.
    """
    artifacts = _construct_model_artifacts(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(False),
            )
        ],
        None,
    )

    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name="Model"
    )

    assert returned_artifacts.sqlalchemy.columns == [
        models_file.types.ColumnArtifacts(
            name="prop_1",
            type="int",
            description=None,
        )
    ]


@pytest.mark.parametrize(
    "artifacts, expected_empty",
    [
        pytest.param(_construct_model_artifacts([], None), True, id="empty"),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(False),
                    )
                ],
                None,
            ),
            False,
            id="single",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_column_empty(artifacts, expected_empty):
    """
    GIVEN artifacts
    WHEN calculate is called with the artifacts
    THEN the given expected columns are added to the artifacts.
    """
    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name="Model"
    )

    assert returned_artifacts.sqlalchemy.empty == expected_empty


@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_arg():
    """
    GIVEN artifacts
    WHEN calculate is called with the artifacts
    THEN the given expected args are added to the artifacts.
    """
    artifacts = _construct_model_artifacts(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(False),
            ),
            (
                "prop_2",
                _construct_simple_property_artifacts(True),
            ),
        ],
        None,
    )

    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name="Model"
    )

    assert returned_artifacts.sqlalchemy.arg.not_required == [
        models_file.types.ColumnArgArtifacts(
            name="prop_1",
            init_type="typing.Optional[int]",
            from_dict_type="typing.Optional[int]",
            default=None,
            read_only=None,
        )
    ]
    assert returned_artifacts.sqlalchemy.arg.required == [
        models_file.types.ColumnArgArtifacts(
            name="prop_2",
            init_type="int",
            from_dict_type="int",
            default=None,
            read_only=None,
        )
    ]


@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_typed_dict_column():
    """
    GIVEN artifacts
    WHEN calculate is called with the artifacts
    THEN the given expected typed dict columns are added to the artifacts.
    """
    artifacts = _construct_model_artifacts(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(False),
            ),
            (
                "prop_2",
                _construct_simple_property_artifacts(True),
            ),
        ],
        None,
    )

    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name="Model"
    )

    assert returned_artifacts.typed_dict.not_required.props == [
        models_file.types.ColumnArtifacts(
            name="prop_1",
            type="int",
            description=None,
        )
    ]
    assert returned_artifacts.typed_dict.required.props == [
        models_file.types.ColumnArtifacts(
            name="prop_2",
            type="int",
            description=None,
        )
    ]


@pytest.mark.parametrize(
    "artifacts, expected_required_empty, expected_not_required_empty",
    [
        pytest.param(_construct_model_artifacts([], None), True, True, id="empty"),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(True),
                    )
                ],
                None,
            ),
            False,
            True,
            id="single required",
        ),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(False),
                    )
                ],
                None,
            ),
            True,
            False,
            id="single not required",
        ),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(False),
                    ),
                    (
                        "prop_2",
                        _construct_simple_property_artifacts(True),
                    ),
                ],
                None,
            ),
            False,
            False,
            id="multiple required and  not required",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_typed_dict_column_empty(
    artifacts, expected_required_empty, expected_not_required_empty
):
    """
    GIVEN artifacts and expected required and not required empty
    WHEN calculate is called with the artifacts
    THEN the typed dict required and not required empty are as expected.
    """
    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name="Model"
    )

    assert returned_artifacts.typed_dict.required.empty == expected_required_empty
    assert (
        returned_artifacts.typed_dict.not_required.empty == expected_not_required_empty
    )


# Table for the name of the required and not required TypedDicts
# +----------------+--------------------+-----------------------+-------------------+
# | required empty | not required empty | required name         | not required name |
# +================+====================+=======================+===================+
# | False          | False              | _<model name>DictBase | <model name>Dict  |
# +----------------+--------------------+-----------------------+-------------------+
# | False          | True               | <model name>Dict      | None              |
# +----------------+--------------------+-----------------------+-------------------+
# | True           | False              | None                  | <model name>Dict  |
# +----------------+--------------------+-----------------------+-------------------+
# | True           | True               | None                  | <model name>Dict  |
# +----------------+--------------------+-----------------------+-------------------+


@pytest.mark.parametrize(
    "artifacts, expected_required_name, expected_not_required_name",
    [
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(False),
                    ),
                    (
                        "prop_2",
                        _construct_simple_property_artifacts(True),
                    ),
                ],
                None,
            ),
            "_ModelDictBase",
            "ModelDict",
            id="required empty: False, not required empty: False",
        ),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(True),
                    ),
                ],
                None,
            ),
            "ModelDict",
            None,
            id="required empty: False, not required empty: True",
        ),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(False),
                    ),
                ],
                None,
            ),
            None,
            "ModelDict",
            id="required empty: True,  not required empty: False",
        ),
        pytest.param(
            _construct_model_artifacts(
                [],
                None,
            ),
            None,
            "ModelDict",
            id="required empty: True,  not required empty: True",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_td_names(
    artifacts, expected_required_name, expected_not_required_name
):
    """
    GIVEN artifacts
    WHEN calculate is called with the artifacts
    THEN the given expected td required and not required names are added to the
        artifacts.
    """
    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name="Model"
    )

    assert returned_artifacts.typed_dict.required.name == expected_required_name
    assert returned_artifacts.typed_dict.not_required.name == expected_not_required_name


# Table for the parent class of the required and not required TypedDicts
# +----------------+--------------------+------------------+-----------------------+
# | required empty | not required empty | required parent  | not required parent   |
# +================+====================+==================+=======================+
# | False          | False              | typing.TypedDict | _<model name>DictBase |
# +----------------+--------------------+------------------+-----------------------+
# | False          | True               | typing.TypedDict | None                  |
# +----------------+--------------------+------------------+-----------------------+
# | True           | False              | None             | typing.TypedDict      |
# +----------------+--------------------+------------------+-----------------------+
# | True           | True               | None             | typing.TypedDict      |
# +----------------+--------------------+------------------+-----------------------+


_EXPECTED_TD_BASE = "typing.TypedDict"
if sys.version_info[1] < 8:
    _EXPECTED_TD_BASE = "typing_extensions.TypedDict"


@pytest.mark.parametrize(
    "artifacts, expected_required_parent, expected_not_required_parent",
    [
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(False),
                    ),
                    (
                        "prop_2",
                        _construct_simple_property_artifacts(True),
                    ),
                ],
                None,
            ),
            _EXPECTED_TD_BASE,
            "_ModelDictBase",
            id="required empty: False, not required empty: False",
        ),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(True),
                    ),
                ],
                None,
            ),
            _EXPECTED_TD_BASE,
            None,
            id="required empty: False, not required empty: True",
        ),
        pytest.param(
            _construct_model_artifacts(
                [
                    (
                        "prop_1",
                        _construct_simple_property_artifacts(False),
                    ),
                ],
                None,
            ),
            None,
            _EXPECTED_TD_BASE,
            id="required empty: True,  not required empty: False",
        ),
        pytest.param(
            _construct_model_artifacts(
                [],
                None,
            ),
            None,
            _EXPECTED_TD_BASE,
            id="required empty: True,  not required empty: True",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_calculate_td_parent(
    artifacts, expected_required_parent, expected_not_required_parent
):
    """
    GIVEN artifacts
    WHEN calculate is called with the artifacts
    THEN the given expected td required and not required parents are added to the
        artifacts.
    """
    returned_artifacts = models_file._artifacts.calculate(
        artifacts=artifacts, name="Model"
    )

    assert (
        returned_artifacts.typed_dict.required.parent_class == expected_required_parent
    )
    artifacts_not_required_parent = (
        returned_artifacts.typed_dict.not_required.parent_class
    )
    assert artifacts_not_required_parent == expected_not_required_parent
