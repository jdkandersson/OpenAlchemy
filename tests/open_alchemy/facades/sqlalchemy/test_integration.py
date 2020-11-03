"""Tests for the SQLAlchemy facade."""

from unittest import mock

import pytest
import sqlalchemy

from open_alchemy import facades
from open_alchemy import types


@pytest.mark.parametrize(
    "name, expected_value", [("Table", sqlalchemy.Table)], ids=["Table"]
)
@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_mapping(name, expected_value):
    """
    GIVEN name and expected value
    WHEN the name is retrieved from facades.sqlalchemy
    THEN the expected value is returned.
    """
    returned_value = getattr(facades.sqlalchemy, name)

    assert returned_value == expected_value


@pytest.mark.parametrize(
    "artifacts, exp_argument, exp_backref, exp_uselist, exp_secondary",
    [
        (types.RelationshipArtifacts("RefModel"), "RefModel", None, None, None),
        (
            types.RelationshipArtifacts(
                "RefModel", types.BackReferenceArtifacts("BackRefModel")
            ),
            "RefModel",
            "BackRefModel",
            None,
            None,
        ),
        (
            types.RelationshipArtifacts(
                "RefModel", types.BackReferenceArtifacts("BackRefModel", True)
            ),
            "RefModel",
            "BackRefModel",
            True,
            None,
        ),
        (
            types.RelationshipArtifacts("RefModel", secondary="association"),
            "RefModel",
            None,
            None,
            "association",
        ),
    ],
    ids=["plain", "backref", "backref and uselist", "secondary"],
)
@pytest.mark.facade
@pytest.mark.sqlalchemy
@pytest.mark.sqlalchemy
def test_construct_relationship_plain(
    artifacts, exp_argument, exp_backref, exp_uselist, exp_secondary
):
    """
    GIVEN given relationship artifacts
    WHEN construct_relationship is called with the artifacts
    THEN a relationship with the given expected argument, backref, uselist and secondary
        is returned.
    """
    relationship = facades.sqlalchemy.construct_relationship(artifacts=artifacts)

    assert relationship.argument == exp_argument
    if exp_backref is None:
        assert relationship.backref is None
    else:
        assert relationship.backref == (exp_backref, {"uselist": exp_uselist})
    assert relationship.secondary == exp_secondary


@pytest.mark.facade
@pytest.mark.sqlalchemy
@pytest.mark.sqlalchemy
def test_construct_relationship_kwargs():
    """
    GIVEN given relationship artifacts with kwargs
    WHEN construct_relationship is called with the artifacts
    THEN a relationship with the kwargs set is returned.
    """
    artifacts = types.RelationshipArtifacts("RefModel", kwargs={"order_by": "id"})

    relationship = facades.sqlalchemy.construct_relationship(artifacts=artifacts)

    assert relationship.order_by == "id"


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct():
    """
    GIVEN tablename, mock base and 2 columns
    WHEN construct is called with the columns and base
    THEN a table with the correct name, columns and metadata is constructed.
    """
    tablename = "association"
    mock_base = mock.MagicMock()
    columns = (
        sqlalchemy.Column(sqlalchemy.Integer, name="column_1"),
        sqlalchemy.Column(sqlalchemy.String, name="column_2"),
    )

    returned_table = facades.sqlalchemy.table(
        tablename=tablename, base=mock_base, columns=columns
    )

    assert returned_table.name == tablename
    assert returned_table.metadata == (mock_base.metadata)
    assert len(returned_table.columns) == 2
    assert isinstance(returned_table.columns["column_1"].type, sqlalchemy.Integer)
    assert isinstance(returned_table.columns["column_2"].type, sqlalchemy.String)
