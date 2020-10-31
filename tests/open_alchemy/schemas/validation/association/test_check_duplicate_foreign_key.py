"""Tests for _check_duplicate_foreign_key function in association validation."""

import pytest

from open_alchemy import types
from open_alchemy.schemas import helpers
from open_alchemy.schemas import validation


class TestCheckDuplicateForeignKey:
    """Tests for _check_duplicate_foreign_key."""

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
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key_1"}
                }
            },
            {},
            True,
            None,
            id="single property",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key_1"},
                    "prop_2": {"x-primary-key": True, "x-foreign-key": "foreign.key_2"},
                    "prop_3": {},
                }
            },
            {},
            True,
            None,
            id="multiple property different",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key_1"},
                    "prop_2": {
                        "allOf": [
                            {"x-primary-key": True, "x-foreign-key": "foreign.key_2"},
                            {"$ref": "#/components/schemas/RefSchema"},
                        ]
                    },
                    "prop_3": {},
                }
            },
            {"RefSchema": {"x-foreign-key": "foreign.key_1"}},
            True,
            None,
            id="multiple property different local ref local first",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key_1"},
                    "prop_2": {
                        "allOf": [
                            {"$ref": "#/components/schemas/RefSchema"},
                            {"x-primary-key": True, "x-foreign-key": "foreign.key_2"},
                        ]
                    },
                    "prop_3": {},
                }
            },
            {"RefSchema": {"x-foreign-key": "foreign.key_1"}},
            True,
            None,
            id="multiple property different local ref ref first",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key_1"},
                    "prop_2": {"x-primary-key": True, "x-foreign-key": "foreign.key_1"},
                    "prop_3": {},
                }
            },
            {},
            False,
            ("prop_1", "prop_2", "foreign.key_1"),
            id="multiple property same first order",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key_1"},
                    "prop_2": {},
                    "prop_3": {"x-primary-key": True, "x-foreign-key": "foreign.key_1"},
                }
            },
            {},
            False,
            ("prop_1", "prop_3", "foreign.key_1"),
            id="multiple property same second order",
        ),
    ]

    @staticmethod
    @pytest.mark.schemas
    @pytest.mark.validate
    @pytest.mark.parametrize("schema, schemas, expected_valid, expected_reasons", TESTS)
    def test_(schema, schemas, expected_valid, expected_reasons):
        """
        GIVEN schema, schemas, and expected valid and reasons
        WHEN _check_duplicate_foreign_key is called with the schema and schemas
        THEN the expected valid and reasons are returned.
        """
        name = "Schema"
        association = helpers.association.TParentPropertySchema(
            parent=types.TNameSchema(name="ParentSchema", schema={}),
            property=types.TNameSchema(name="PropertySchema", schema={}),
        )

        returned_result = validation.association._check_duplicate_foreign_key(
            name=name, schema=schema, association=association, schemas=schemas
        )

        assert returned_result.valid == expected_valid
        if expected_reasons is not None:
            expected_reasons = (
                *expected_reasons,
                name,
                association.parent.name,
                association.property.name,
                "duplicate",
                "foreign key",
            )

            for reason in expected_reasons:
                assert reason in returned_result.reason
