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


def _construct_simple_property_artifacts(type_, format_, default):
    """Construct the artifacts for a simple property."""
    return schemas_artifacts.types.SimplePropertyArtifacts(
        type=helpers.property_.type_.Type.SIMPLE,
        open_api=schemas_artifacts.types.OpenApiSimplePropertyArtifacts(
            type=type_,
            format=format_,
            max_length=None,
            nullable=False,
            default=default,
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
        required=False,
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
        required=False,
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


def _construct_backrefs_item():
    """Construct a model backref item."""
    return schemas_artifacts.types.ModelBackrefArtifacts(
        type=schemas_artifacts.types.BackrefSubType.OBJECT,
        child="Child1",
    )


MAP_DEAULT_TESTS = [
    pytest.param(_construct_relationship_property_artifacts(), None, id="relationship"),
    pytest.param(_construct_json_property_artifacts(), None, id="json"),
    pytest.param(_construct_backref_property_artifacts(), None, id="backref"),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="integer", format_=None, default=None
        ),
        None,
        id="simple integer default None",
    ),
    pytest.param(
        _construct_simple_property_artifacts(type_="integer", format_=None, default=1),
        1,
        id="simple integer format None default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="integer", format_="int32", default=1
        ),
        1,
        id="simple integer format int32 default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="integer", format_="int64", default=1
        ),
        1,
        id="simple integer format int64 default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(type_="number", format_=None, default=1.1),
        1.1,
        id="simple number format None default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="number", format_="float", default=1.1
        ),
        1.1,
        id="simple number format float default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string", format_=None, default='value "1'
        ),
        '"value \\"1"',
        id="simple string format None default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string", format_="unsupported", default='value "1'
        ),
        '"value \\"1"',
        id="simple string format unsupported default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string", format_="password", default='value "1'
        ),
        '"value \\"1"',
        id="simple string format password default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string", format_="byte", default='value "1'
        ),
        '"value \\"1"',
        id="simple string format byte default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string", format_="binary", default='value "1'
        ),
        'b"value \\"1"',
        id="simple string format binary default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string", format_="date", default="2000-01-01"
        ),
        "datetime.date(2000, 1, 1)",
        id="simple string format date default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="string", format_="date-time", default="2000-01-01T01:01:01"
        ),
        "datetime.datetime(2000, 1, 1, 1, 1, 1)",
        id="simple string format date-time default defined",
    ),
    pytest.param(
        _construct_simple_property_artifacts(
            type_="boolean", format_=None, default=True
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
