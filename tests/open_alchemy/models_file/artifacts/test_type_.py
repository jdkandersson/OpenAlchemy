"""Tests for type_."""
# pylint: disable=protected-access

import pytest

from open_alchemy import helpers as oa_helpers
from open_alchemy import models_file
from open_alchemy.schemas import artifacts as schemas_artifacts
from open_alchemy.schemas import helpers


def _construct_simple_artifacts(
    *, type_, format_=None, nullable=None, generated=None, default=None, required=False
):
    """Construct the artifacts for a simple property."""
    return schemas_artifacts.types.SimplePropertyArtifacts(
        type=helpers.property_.type_.Type.SIMPLE,
        open_api=schemas_artifacts.types.OpenApiSimplePropertyArtifacts(
            type=type_,
            format=format_,
            max_length=None,
            nullable=nullable,
            default=default,
            read_only=None,
            write_only=None,
        ),
        extension=schemas_artifacts.types.ExtensionSimplePropertyArtifacts(
            primary_key=False,
            autoincrement=generated,
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


def _construct_json_artifacts(required=False):
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
        required=required,
        description=None,
    )


def _construct_many_to_one_relationship_artifacts(required=False, nullable=None):
    """Construct many-to-one relationship artifacts."""
    return schemas_artifacts.types.ManyToOneRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.MANY_TO_ONE,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=required,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=nullable,
    )


def _construct_one_to_one_relationship_artifacts(required=False, nullable=None):
    """Construct one-to-one relationship artifacts."""
    return schemas_artifacts.types.OneToOneRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.ONE_TO_ONE,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=required,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=nullable,
    )


def _construct_one_to_many_relationship_artifacts(required=False):
    """Construct one-to-many relationship artifacts."""
    return schemas_artifacts.types.OneToManyRelationshipPropertyArtifacts(
        type=helpers.property_.type_.Type.RELATIONSHIP,
        schema={},  # type: ignore
        sub_type=oa_helpers.relationship.Type.ONE_TO_MANY,
        parent="RefModel",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=required,
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
    )


def _construct_many_to_many_relationship_artifacts(required=False):
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
        required=required,
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


@pytest.mark.parametrize(
    "artifacts, expected_type",
    [
        pytest.param(
            _construct_simple_artifacts(type_="integer", nullable=False),
            "int",
            id="simple integer no format",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="integer", format_="int32", nullable=False
            ),
            "int",
            id="simple integer int32 format",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="integer", format_="int64", nullable=False
            ),
            "int",
            id="simple integer int64 format",
        ),
        pytest.param(
            _construct_simple_artifacts(type_="number", nullable=False),
            "float",
            id="simple number no format",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="number", format_="float", nullable=False
            ),
            "float",
            id="simple number float format",
        ),
        pytest.param(
            _construct_simple_artifacts(type_="string", nullable=False),
            "str",
            id="simple string no format",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="string", format_="password", nullable=False
            ),
            "str",
            id="simple string password format",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="string", format_="unsupported", nullable=False
            ),
            "str",
            id="simple string unsupported format",
        ),
        pytest.param(
            _construct_simple_artifacts(type_="string", format_="byte", nullable=False),
            "str",
            id="simple string byte format",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="string", format_="binary", nullable=False
            ),
            "bytes",
            id="simple string binary format",
        ),
        pytest.param(
            _construct_simple_artifacts(type_="string", format_="date", nullable=False),
            "datetime.date",
            id="simple string date format",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="string", format_="date-time", nullable=False
            ),
            "datetime.datetime",
            id="simple string date-time format",
        ),
        pytest.param(
            _construct_simple_artifacts(type_="boolean", nullable=False),
            "bool",
            id="simple boolean no format",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="integer",
                nullable=None,
                required=False,
                generated=None,
                default=None,
            ),
            "typing.Optional[int]",
            id="simple nullable and required None",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="integer",
                nullable=None,
                required=True,
                generated=None,
                default=None,
            ),
            "int",
            id="simple nullable None required True",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="integer",
                nullable=None,
                required=False,
                generated=True,
                default=None,
            ),
            "int",
            id="simple nullable None generated True",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="integer",
                nullable=None,
                required=False,
                generated=False,
                default=None,
            ),
            "typing.Optional[int]",
            id="simple nullable None generated False",
        ),
        pytest.param(
            _construct_simple_artifacts(
                type_="integer",
                nullable=None,
                required=False,
                generated=None,
                default=1,
            ),
            "int",
            id="simple nullable None default given",
        ),
        pytest.param(
            _construct_json_artifacts(),
            "typing.Any",
            id="json",
        ),
        pytest.param(
            _construct_many_to_one_relationship_artifacts(nullable=None),
            'typing.Optional["TRefModel"]',
            id="relationship many-to-one nullable None",
        ),
        pytest.param(
            _construct_many_to_one_relationship_artifacts(nullable=False),
            '"TRefModel"',
            id="relationship many-to-one nullable False",
        ),
        pytest.param(
            _construct_many_to_one_relationship_artifacts(nullable=True),
            'typing.Optional["TRefModel"]',
            id="relationship many-to-one nullable True",
        ),
        pytest.param(
            _construct_many_to_one_relationship_artifacts(required=False),
            'typing.Optional["TRefModel"]',
            id="relationship many-to-one required False",
        ),
        pytest.param(
            _construct_many_to_one_relationship_artifacts(required=True),
            '"TRefModel"',
            id="relationship many-to-one required True",
        ),
        pytest.param(
            _construct_one_to_one_relationship_artifacts(nullable=None),
            'typing.Optional["TRefModel"]',
            id="relationship one-to-one nullable None",
        ),
        pytest.param(
            _construct_one_to_one_relationship_artifacts(nullable=False),
            '"TRefModel"',
            id="relationship one-to-one nullable False",
        ),
        pytest.param(
            _construct_one_to_one_relationship_artifacts(nullable=True),
            'typing.Optional["TRefModel"]',
            id="relationship one-to-one nullable True",
        ),
        pytest.param(
            _construct_one_to_one_relationship_artifacts(required=False),
            'typing.Optional["TRefModel"]',
            id="relationship one-to-one required False",
        ),
        pytest.param(
            _construct_one_to_one_relationship_artifacts(required=True),
            '"TRefModel"',
            id="relationship one-to-one required True",
        ),
        pytest.param(
            _construct_one_to_many_relationship_artifacts(required=False),
            'typing.Sequence["TRefModel"]',
            id="relationship one-to-many required False",
        ),
        pytest.param(
            _construct_one_to_many_relationship_artifacts(required=True),
            'typing.Sequence["TRefModel"]',
            id="relationship one-to-many required True",
        ),
        pytest.param(
            _construct_many_to_many_relationship_artifacts(required=False),
            'typing.Sequence["TRefModel"]',
            id="relationship many-to-many required False",
        ),
        pytest.param(
            _construct_many_to_many_relationship_artifacts(required=True),
            'typing.Sequence["TRefModel"]',
            id="relationship many-to-many required True",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_model(artifacts, expected_type):
    """
    GIVEN artifacts
    WHEN model is called with the artifacts
    THEN the expected type is returned.
    """
    returned_type = models_file._artifacts._type.model(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "artifacts, expected_type",
    [
        pytest.param(
            _construct_simple_artifacts(type_="integer"),
            "typing.Optional[int]",
            id="simple plain",
        ),
        pytest.param(
            _construct_simple_artifacts(type_="string", format_="binary"),
            "typing.Optional[str]",
            id="simple binary",
        ),
        pytest.param(
            _construct_simple_artifacts(type_="string", format_="date"),
            "typing.Optional[str]",
            id="simple date",
        ),
        pytest.param(
            _construct_simple_artifacts(type_="string", format_="date-time"),
            "typing.Optional[str]",
            id="simple date-time",
        ),
        pytest.param(
            _construct_json_artifacts(),
            "typing.Any",
            id="json",
        ),
        pytest.param(
            _construct_many_to_one_relationship_artifacts(),
            'typing.Optional["RefModelDict"]',
            id="relationship many-to-one",
        ),
        pytest.param(
            _construct_one_to_one_relationship_artifacts(),
            'typing.Optional["RefModelDict"]',
            id="relationship one-to-one",
        ),
        pytest.param(
            _construct_one_to_many_relationship_artifacts(),
            'typing.Sequence["RefModelDict"]',
            id="relationship one-to-many",
        ),
        pytest.param(
            _construct_many_to_many_relationship_artifacts(),
            'typing.Sequence["RefModelDict"]',
            id="relationship many-to-many",
        ),
        pytest.param(
            _construct_backref_property_artifacts(
                schemas_artifacts.types.BackrefSubType.OBJECT
            ),
            "typing.Optional[typing.Dict[str, typing.Union[int, float, str, bool]]]",
            id="backref object",
        ),
        pytest.param(
            _construct_backref_property_artifacts(
                schemas_artifacts.types.BackrefSubType.ARRAY
            ),
            "typing.Sequence[typing.Dict[str, typing.Union[int, float, str, bool]]]",
            id="backref array",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_dict(artifacts, expected_type):
    """
    GIVEN artifacts and expected type
    WHEN typed_dict is called with the artifacts
    THEN the given expected type is returned.
    """
    returned_type = models_file._artifacts._type.typed_dict(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "nullable, required, default, expected_type",
    [
        pytest.param(False, True, None, "int", id="not nullable required"),
        pytest.param(
            False, False, None, "typing.Optional[int]", id="not nullable not required"
        ),
        pytest.param(True, True, None, "typing.Optional[int]", id="nullable required"),
        pytest.param(
            True, False, None, "typing.Optional[int]", id="nullable not required"
        ),
        pytest.param(False, False, 1, "int", id="not nullable default"),
        pytest.param(True, False, 1, "int", id="nullable default"),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_arg_init(nullable, required, default, expected_type):
    """
    GIVEN nullable and required
    WHEN arg_init is called with the nullable and required
    THEN the expected type is returned.
    """
    artifacts = _construct_simple_artifacts(
        type_="integer", nullable=nullable, required=required, default=default
    )

    returned_type = models_file._artifacts._type.arg_init(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "artifacts, expected_type",
    [
        pytest.param(
            _construct_simple_artifacts(type_="integer", required=True),
            "int",
            id="plain",
        ),
        pytest.param(
            _construct_json_artifacts(required=True),
            "typing.Any",
            id="json",
        ),
        pytest.param(
            _construct_many_to_one_relationship_artifacts(required=True),
            '"RefModelDict"',
            id="relationship many-to-one",
        ),
        pytest.param(
            _construct_one_to_one_relationship_artifacts(required=True),
            '"RefModelDict"',
            id="relationship one-to-one",
        ),
        pytest.param(
            _construct_one_to_many_relationship_artifacts(required=True),
            'typing.Sequence["RefModelDict"]',
            id="relationship one-to-many",
        ),
        pytest.param(
            _construct_many_to_many_relationship_artifacts(required=True),
            'typing.Sequence["RefModelDict"]',
            id="relationship many-to-many",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.artifacts
def test_arg_from_dict(artifacts, expected_type):
    """
    GIVEN None format and required, False nullable and de_ref and given type
    WHEN arg_from_dict is called with the type, format, nullable, required and de_ref
    THEN the given expected type is returned.
    """
    returned_type = models_file._artifacts._type.arg_from_dict(artifacts=artifacts)

    assert returned_type == expected_type
