"""Tests for _check_primary_key_no_foreign_key function in association validation."""

import pytest

from open_alchemy import types
from open_alchemy.schemas import helpers
from open_alchemy.schemas import validation


class TestCheckPrimaryKeyNoForeignKey:
    """Tests for _check_primary_key_no_foreign_key."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param(
            {"properties": {"prop_1": {}}},
            {},
            True,
            None,
            id="single property not primary key",
        ),
        pytest.param(
            {"properties": {"prop_1": {"x-primary-key": True}}},
            {},
            False,
            ("prop_1",),
            id="single property primary key no foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key"}
                }
            },
            {},
            True,
            None,
            id="single property primary key with foreign key",
        ),
        pytest.param(
            {"properties": {"prop_1": {"$ref": "#/components/schemas/RefSchema"}}},
            {"RefSchema": {"x-primary-key": True, "x-foreign-key": "foreign.key"}},
            True,
            None,
            id="single property $ref primary key with foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "allOf": [
                            {"x-primary-key": True, "x-foreign-key": "foreign.key"}
                        ]
                    }
                }
            },
            {},
            True,
            None,
            id="single property allOf primary key with foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True},
                    "prop_2": {"x-primary-key": True},
                }
            },
            {},
            False,
            ("prop_1",),
            id="multiple property all primary key no foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True},
                    "prop_2": {"x-primary-key": True, "x-foreign-key": "foreign.key"},
                }
            },
            {},
            False,
            ("prop_1",),
            id="multiple property first primary key no foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key"},
                    "prop_2": {"x-primary-key": True},
                }
            },
            {},
            False,
            ("prop_2",),
            id="multiple property second primary key no foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key"},
                    "prop_2": {"x-primary-key": True, "x-foreign-key": "foreign.key"},
                }
            },
            {},
            True,
            None,
            id="multiple property all second primary key foreign key",
        ),
    ]

    @staticmethod
    @pytest.mark.schemas
    @pytest.mark.validate
    @pytest.mark.parametrize("schema, schemas, expected_valid, expected_reasons", TESTS)
    def test_(schema, schemas, expected_valid, expected_reasons):
        """
        GIVEN schema, schemas, and expected valid and reasons
        WHEN _check_primary_key_no_foreign_key is called with the schema and schemas
        THEN the expected valid and reasons are returned.
        """
        name = "Schema"
        association = helpers.association.TParentPropertySchema(
            parent=types.TNameSchema(name="ParentSchema", schema={}),
            property=types.TNameSchema(name="PropertySchema", schema={}),
        )

        returned_result = validation.association._check_primary_key_no_foreign_key(
            name=name, schema=schema, association=association, schemas=schemas
        )

        assert returned_result.valid == expected_valid
        if expected_reasons is not None:
            expected_reasons = (
                *expected_reasons,
                name,
                association.parent.name,
                association.property.name,
                "primary key",
                "define",
                "foreign key",
            )

            for reason in expected_reasons:
                assert reason in returned_result.reason
