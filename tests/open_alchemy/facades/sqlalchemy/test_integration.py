"""Tests for the SQLAlchemy facade."""

import pytest
import sqlalchemy

from open_alchemy import facades
from open_alchemy import types


@pytest.mark.parametrize(
    "name, expected_value", [("Table", sqlalchemy.Table)], ids=["Table"]
)
@pytest.mark.facade
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
def test_construct_relationship_plain(
    artifacts, exp_argument, exp_backref, exp_uselist, exp_secondary
):
    """
    GIVEN given relationship artifacts
    WHEN construct_relationship is called with the artifacts
    THEN a relationship with the given expected argument, backref, uselist and secondary
        is returned.
    """
    relationship = facades.sqlalchemy.relationship(artifacts=artifacts)

    assert relationship.argument == exp_argument
    if exp_backref is None:
        assert relationship.backref is None
    else:
        assert relationship.backref == (exp_backref, {"uselist": exp_uselist})
    assert relationship.secondary == exp_secondary
