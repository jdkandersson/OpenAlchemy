"""Tests for _check_2_or_fewer_primary_key function in association validation."""

import pytest

from open_alchemy import types
from open_alchemy.schemas import helpers
from open_alchemy.schemas import validation


class TestCheck2OrFewerPrimaryKey:
    """Tests for _check_2_or_fewer_primary_key."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param(
            {"properties": {"prop_1": {}}},
            {},
            True,
            id="single property not primary key",
        ),
        pytest.param(
            {"properties": {"prop_1": {"x-primary-key": True}}},
            {},
            True,
            id="single property primary key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {},
                    "prop_2": {"x-primary-key": True},
                    "prop_3": {"x-primary-key": True},
                }
            },
            {},
            True,
            id="multiple property 2 primary key first",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True},
                    "prop_2": {},
                    "prop_3": {"x-primary-key": True},
                }
            },
            {},
            True,
            id="multiple property 2 primary key middle",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True},
                    "prop_2": {"x-primary-key": True},
                    "prop_3": {},
                }
            },
            {},
            True,
            id="multiple property 2 primary key last",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True},
                    "prop_2": {"x-primary-key": True},
                    "prop_3": {"x-primary-key": True},
                }
            },
            {},
            False,
            id="multiple property all primary key",
        ),
    ]

    @staticmethod
    @pytest.mark.schemas
    @pytest.mark.validate
    @pytest.mark.parametrize("schema, schemas, expected_valid", TESTS)
    def test_(schema, schemas, expected_valid):
        """
        GIVEN schema, schemas, and expected valid
        WHEN _check_2_or_fewer_primary_key is called with the schema and schemas
        THEN the expected valid and reasons are returned.
        """
        name = "Schema"
        association = helpers.association.TParentPropertySchema(
            parent=types.TNameSchema(name="ParentSchema", schema={}),
            property=types.TNameSchema(name="PropertySchema", schema={}),
        )

        returned_result = validation.association._check_2_or_fewer_primary_key(
            name=name, schema=schema, association=association, schemas=schemas
        )

        assert returned_result.valid == expected_valid
        if not expected_valid:
            expected_reasons = (
                name,
                association.parent.name,
                association.property.name,
                "too many",
                "primary key",
            )

            for reason in expected_reasons:
                assert reason in returned_result.reason
