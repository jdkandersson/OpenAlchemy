"""Tests for _combine_defined_expected_schema association schemas function."""

import pytest

from open_alchemy import types
from open_alchemy.schemas import association


class TestGetTablenameForeignKeys:
    """Tests for _combine_defined_expected_schema."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param(
            association._TParentNameForeignKeys(
                parent_name="Parent1", foreign_keys=set()
            ),
            types.TNameSchema(
                name="Association1",
                schema={
                    "properties": {
                        "prop_1": {"x-foreign-key": "foreign.key1"},
                        "prop_2": {"x-foreign-key": "foreign.key2"},
                    },
                    "required": ["prop_1", "prop_2"],
                },
            ),
            {"Parent1": {"key": "value"}},
            types.TNameSchema(
                name="Parent1",
                schema={
                    "allOf": [
                        {
                            "properties": {
                                "prop_1": {"x-foreign-key": "foreign.key1"},
                                "prop_2": {"x-foreign-key": "foreign.key2"},
                            }
                        },
                        {"key": "value"},
                    ]
                },
            ),
            id="foreign key empty",
        ),
        pytest.param(
            association._TParentNameForeignKeys(
                parent_name="Parent2", foreign_keys=set()
            ),
            types.TNameSchema(
                name="Association1",
                schema={
                    "properties": {
                        "prop_1": {"x-foreign-key": "foreign.key1"},
                        "prop_2": {"x-foreign-key": "foreign.key2"},
                    },
                    "required": ["prop_1", "prop_2"],
                },
            ),
            {"Parent2": {"key_2": "value 2"}},
            types.TNameSchema(
                name="Parent2",
                schema={
                    "allOf": [
                        {
                            "properties": {
                                "prop_1": {"x-foreign-key": "foreign.key1"},
                                "prop_2": {"x-foreign-key": "foreign.key2"},
                            }
                        },
                        {"key_2": "value 2"},
                    ]
                },
            ),
            id="foreign key empty different parent",
        ),
        pytest.param(
            association._TParentNameForeignKeys(
                parent_name="Parent1", foreign_keys={"foreign.key3"}
            ),
            types.TNameSchema(
                name="Association1",
                schema={
                    "properties": {
                        "prop_1": {"x-foreign-key": "foreign.key1"},
                        "prop_2": {"x-foreign-key": "foreign.key2"},
                    },
                    "required": ["prop_1", "prop_2"],
                },
            ),
            {"Parent1": {"key": "value"}},
            types.TNameSchema(
                name="Parent1",
                schema={
                    "allOf": [
                        {
                            "properties": {
                                "prop_1": {"x-foreign-key": "foreign.key1"},
                                "prop_2": {"x-foreign-key": "foreign.key2"},
                            }
                        },
                        {"key": "value"},
                    ]
                },
            ),
            id="single foreign key miss",
        ),
        pytest.param(
            association._TParentNameForeignKeys(
                parent_name="Parent1", foreign_keys={"foreign.key1"}
            ),
            types.TNameSchema(
                name="Association1",
                schema={
                    "properties": {
                        "prop_1": {"x-foreign-key": "foreign.key1"},
                        "prop_2": {"x-foreign-key": "foreign.key2"},
                    },
                    "required": ["prop_1", "prop_2"],
                },
            ),
            {"Parent1": {"key": "value"}},
            types.TNameSchema(
                name="Parent1",
                schema={
                    "allOf": [
                        {
                            "properties": {
                                "prop_2": {"x-foreign-key": "foreign.key2"},
                            }
                        },
                        {"key": "value"},
                    ]
                },
            ),
            id="single foreign key first hit",
        ),
        pytest.param(
            association._TParentNameForeignKeys(
                parent_name="Parent1", foreign_keys={"foreign.key2"}
            ),
            types.TNameSchema(
                name="Association1",
                schema={
                    "properties": {
                        "prop_1": {"x-foreign-key": "foreign.key1"},
                        "prop_2": {"x-foreign-key": "foreign.key2"},
                    },
                    "required": ["prop_1", "prop_2"],
                },
            ),
            {"Parent1": {"key": "value"}},
            types.TNameSchema(
                name="Parent1",
                schema={
                    "allOf": [
                        {
                            "properties": {
                                "prop_1": {"x-foreign-key": "foreign.key1"},
                            }
                        },
                        {"key": "value"},
                    ]
                },
            ),
            id="single foreign key second hit",
        ),
        pytest.param(
            association._TParentNameForeignKeys(
                parent_name="Parent1", foreign_keys={"foreign.key1", "foreign.key2"}
            ),
            types.TNameSchema(
                name="Association1",
                schema={
                    "properties": {
                        "prop_1": {"x-foreign-key": "foreign.key1"},
                        "prop_2": {"x-foreign-key": "foreign.key2"},
                    },
                    "required": ["prop_1", "prop_2"],
                },
            ),
            {"Parent1": {"key": "value"}},
            types.TNameSchema(
                name="Parent1",
                schema={
                    "allOf": [
                        {"properties": {}},
                        {"key": "value"},
                    ]
                },
            ),
            id="multiple foreign key all hit",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize(
        "parent_name_foreign_keys, expected_schema, schemas, expected_returned_schema",
        TESTS,
    )
    @pytest.mark.schemas
    @pytest.mark.association
    def test_(
        parent_name_foreign_keys, expected_schema, schemas, expected_returned_schema
    ):
        """
        GIVEN parent name and foreign keys, expected schema and expected returned schema
        WHEN _combine_defined_expected_schema is called with the parent name and foreign
            keys and expected schema
        THEN the expected returned schema is returned.
        """
        returned_schema = association._combine_defined_expected_schema(
            parent_name_foreign_keys=parent_name_foreign_keys,
            expected_schema=expected_schema,
            schemas=schemas,
        )

        assert returned_schema == expected_returned_schema
