"""Tests for argument artifacts."""

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
    type_, format_, default, dict_ignore, read_only, required
):
    """Construct the artifacts for a simple property."""
    return schemas_artifacts.types.SimplePropertyArtifacts(
        type=helpers.property_.type_.Type.SIMPLE,
        open_api=schemas_artifacts.types.OpenApiSimplePropertyArtifacts(
            type=type_,
            format=format_,
            max_length=None,
            nullable=False,
            default=default,
            read_only=read_only,
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
        required=required,
        description=None,
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


def _construct_relationship_property_artifacts():
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
        required=True,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=False,
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


MAP_DEAULT_TESTS = [
    pytest.param(_construct_relationship_property_artifacts(), None, id="relationship"),
    pytest.param(_construct_json_property_artifacts(), None, id="json"),
    pytest.param(_construct_backref_property_artifacts(), None, id="backref"),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="integer",
            format_=None,
            default=None,
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        None,
        id="simple integer default None",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="integer",
            format_=None,
            default=1,
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        1,
        id="simple integer format None default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="integer",
            format_="int32",
            default=1,
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        1,
        id="simple integer format int32 default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="integer",
            format_="int64",
            default=1,
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        1,
        id="simple integer format int64 default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="number",
            format_=None,
            default=1.1,
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        1.1,
        id="simple number format None default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="number",
            format_="float",
            default=1.1,
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        1.1,
        id="simple number format float default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string",
            format_=None,
            default='value "1',
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        '"value \\"1"',
        id="simple string format None default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string",
            format_="unsupported",
            default='value "1',
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        '"value \\"1"',
        id="simple string format unsupported default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string",
            format_="password",
            default='value "1',
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        '"value \\"1"',
        id="simple string format password default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string",
            format_="byte",
            default='value "1',
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        '"value \\"1"',
        id="simple string format byte default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string",
            format_="binary",
            default='value "1',
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        'b"value \\"1"',
        id="simple string format binary default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string",
            format_="date",
            default="2000-01-01",
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        "datetime.date(2000, 1, 1)",
        id="simple string format date default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string",
            format_="date-time",
            default="2000-01-01T01:01:01",
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        "datetime.datetime(2000, 1, 1, 1, 1, 1)",
        id="simple string format date-time default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="boolean",
            format_=None,
            default=True,
            dict_ignore=None,
            read_only=None,
            required=True,
        ),
        True,
        id="simple boolean default defined",
    ),
]


@pytest.mark.parametrize("artifacts, expected_default", MAP_DEAULT_TESTS)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_map_default(artifacts, expected_default):
    """
    GIVEN artifacts and expected default value
    WHEN _map_default is called with the artifacts
    THEN the expected default is returned.
    """
    returned_default = models_file._artifacts._args._map_default(artifacts=artifacts)

    assert returned_default == expected_default


_CALCULATE_TESTS = [
    pytest.param([], [], id="empty"),
    pytest.param(
        [("prop_1", _construct_backref_property_artifacts())], [], id="single backref"
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    type_="integer",
                    format_=None,
                    default=None,
                    dict_ignore=True,
                    read_only=None,
                    required=True,
                ),
            )
        ],
        [],
        id="single simple dict ignore",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    type_="integer",
                    format_=None,
                    default=None,
                    dict_ignore=None,
                    read_only=None,
                    required=True,
                ),
            )
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=None,
            ),
        ],
        id="single simple read only None",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    type_="integer",
                    format_=None,
                    default=None,
                    dict_ignore=None,
                    read_only=False,
                    required=True,
                ),
            )
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=False,
            ),
        ],
        id="single simple read only False",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    type_="integer",
                    format_=None,
                    default=None,
                    dict_ignore=None,
                    read_only=True,
                    required=True,
                ),
            )
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=True,
            ),
        ],
        id="single simple read only True",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    type_="integer",
                    format_=None,
                    default=None,
                    dict_ignore=None,
                    read_only=None,
                    required=True,
                ),
            )
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=None,
            ),
        ],
        id="single simple default None",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    type_="integer",
                    format_=None,
                    default=1,
                    dict_ignore=None,
                    read_only=None,
                    required=True,
                ),
            )
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=1,
                read_only=None,
            ),
        ],
        id="single simple default defined",
    ),
    pytest.param(
        [("prop_1", _construct_json_property_artifacts())],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="typing.Optional[typing.Any]",
                from_dict_type="typing.Optional[typing.Any]",
                default=None,
                read_only=None,
            ),
        ],
        id="single json",
    ),
    pytest.param(
        [("prop_1", _construct_relationship_property_artifacts())],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type='"TRefModel"',
                from_dict_type='"RefModelDict"',
                default=None,
                read_only=None,
            ),
        ],
        id="single relationship",
    ),
    pytest.param(
        [
            (
                "prop_1",
                _construct_simple_property_artifacts(
                    type_="integer",
                    format_=None,
                    default=None,
                    dict_ignore=None,
                    read_only=None,
                    required=True,
                ),
            ),
            (
                "prop_2",
                _construct_simple_property_artifacts(
                    type_="string",
                    format_=None,
                    default=None,
                    dict_ignore=None,
                    read_only=None,
                    required=True,
                ),
            ),
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=None,
            ),
            models_file.types.ColumnArgArtifacts(
                name="prop_2",
                init_type="str",
                from_dict_type="str",
                default=None,
                read_only=None,
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
    returned_columns = models_file.artifacts._args._calculate(artifacts=artifacts)

    assert list(returned_columns) == expected_columns


CALCULATE_TESTS = [
    pytest.param(_construct_model_artifacts([], []), [], [], id="empty"),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        type_="integer",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=True,
                    ),
                )
            ],
            [],
        ),
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=None,
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
                        type_="integer",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=False,
                    ),
                )
            ],
            [],
        ),
        [],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="typing.Optional[int]",
                from_dict_type="typing.Optional[int]",
                default=None,
                read_only=None,
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
                        type_="integer",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=True,
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        type_="string",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=True,
                    ),
                ),
            ],
            [],
        ),
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=None,
            ),
            models_file.types.ColumnArgArtifacts(
                name="prop_2",
                init_type="str",
                from_dict_type="str",
                default=None,
                read_only=None,
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
                        type_="integer",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=False,
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        type_="string",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=True,
                    ),
                ),
            ],
            [],
        ),
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_2",
                init_type="str",
                from_dict_type="str",
                default=None,
                read_only=None,
            )
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="typing.Optional[int]",
                from_dict_type="typing.Optional[int]",
                default=None,
                read_only=None,
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
                        type_="integer",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=True,
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        type_="string",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=False,
                    ),
                ),
            ],
            [],
        ),
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=None,
            ),
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_2",
                init_type="typing.Optional[str]",
                from_dict_type="typing.Optional[str]",
                default=None,
                read_only=None,
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
                        type_="integer",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=False,
                    ),
                ),
                (
                    "prop_2",
                    _construct_simple_property_artifacts(
                        type_="string",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=False,
                    ),
                ),
            ],
            [],
        ),
        [],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="typing.Optional[int]",
                from_dict_type="typing.Optional[int]",
                default=None,
                read_only=None,
            ),
            models_file.types.ColumnArgArtifacts(
                name="prop_2",
                init_type="typing.Optional[str]",
                from_dict_type="typing.Optional[str]",
                default=None,
                read_only=None,
            ),
        ],
        id="multiple not required",
    ),
    pytest.param(
        _construct_model_artifacts(
            [],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        type_=schemas_artifacts.types.BackrefSubType.OBJECT,
                        child="Child1",
                    ),
                )
            ],
        ),
        [],
        [
            models_file.types.ColumnArgArtifacts(
                name="backref_1",
                init_type='typing.Optional["TChild1"]',
                from_dict_type="",
                default=None,
                read_only=True,
            )
        ],
        id="single backrefs object",
    ),
    pytest.param(
        _construct_model_artifacts(
            [],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        type_=schemas_artifacts.types.BackrefSubType.ARRAY,
                        child="Child1",
                    ),
                )
            ],
        ),
        [],
        [
            models_file.types.ColumnArgArtifacts(
                name="backref_1",
                init_type='typing.Optional[typing.Sequence["TChild1"]]',
                from_dict_type="",
                default=None,
                read_only=True,
            )
        ],
        id="single backrefs array",
    ),
    pytest.param(
        _construct_model_artifacts(
            [],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        type_=schemas_artifacts.types.BackrefSubType.OBJECT,
                        child="Child1",
                    ),
                ),
                (
                    "backref_2",
                    _construct_backrefs_item(
                        type_=schemas_artifacts.types.BackrefSubType.OBJECT,
                        child="Child2",
                    ),
                ),
            ],
        ),
        [],
        [
            models_file.types.ColumnArgArtifacts(
                name="backref_1",
                init_type='typing.Optional["TChild1"]',
                from_dict_type="",
                default=None,
                read_only=True,
            ),
            models_file.types.ColumnArgArtifacts(
                name="backref_2",
                init_type='typing.Optional["TChild2"]',
                from_dict_type="",
                default=None,
                read_only=True,
            ),
        ],
        id="multiple backrefs",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        type_="integer",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=True,
                    ),
                )
            ],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        type_=schemas_artifacts.types.BackrefSubType.OBJECT,
                        child="Child1",
                    ),
                )
            ],
        ),
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="int",
                from_dict_type="int",
                default=None,
                read_only=None,
            ),
        ],
        [
            models_file.types.ColumnArgArtifacts(
                name="backref_1",
                init_type='typing.Optional["TChild1"]',
                from_dict_type="",
                default=None,
                read_only=True,
            )
        ],
        id="single properties required single backrefs object",
    ),
    pytest.param(
        _construct_model_artifacts(
            [
                (
                    "prop_1",
                    _construct_simple_property_artifacts(
                        type_="integer",
                        format_=None,
                        dict_ignore=False,
                        default=None,
                        read_only=None,
                        required=False,
                    ),
                )
            ],
            [
                (
                    "backref_1",
                    _construct_backrefs_item(
                        type_=schemas_artifacts.types.BackrefSubType.OBJECT,
                        child="Child1",
                    ),
                )
            ],
        ),
        [],
        [
            models_file.types.ColumnArgArtifacts(
                name="prop_1",
                init_type="typing.Optional[int]",
                from_dict_type="typing.Optional[int]",
                default=None,
                read_only=None,
            ),
            models_file.types.ColumnArgArtifacts(
                name="backref_1",
                init_type='typing.Optional["TChild1"]',
                from_dict_type="",
                default=None,
                read_only=True,
            ),
        ],
        id="single properties not required single backrefs object",
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
    returned_columns = models_file.artifacts._args.calculate(artifacts=artifacts)

    assert returned_columns.required == expected_required_columns
    assert returned_columns.not_required == expected_not_required_columns
