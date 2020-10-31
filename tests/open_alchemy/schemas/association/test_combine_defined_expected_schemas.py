"""Tests for _combine_defined_expected_schemas association schemas function."""

import pytest

from open_alchemy import types
from open_alchemy.schemas import association


class TestCombineDefinedExpectedSchemas:
    """Tests for _combine_defined_expected_schemas."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param([], {}, [], id="empty"),
        pytest.param(
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign.key1"},
                            "prop_2": {"x-foreign-key": "foreign.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                )
            ],
            {},
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign.key1"},
                            "prop_2": {"x-foreign-key": "foreign.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                )
            ],
            id="single not defined",
        ),
        pytest.param(
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign.key1"},
                            "prop_2": {"x-foreign-key": "foreign.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                )
            ],
            {
                "Schema1": {
                    "x-tablename": "association",
                    "properties": {"prop_1": {"x-foreign-key": "foreign.key1"}},
                }
            },
            [
                types.TNameSchema(
                    name="Schema1",
                    schema={
                        "allOf": [
                            {
                                "x-tablename": "association",
                                "properties": {
                                    "prop_2": {"x-foreign-key": "foreign.key2"},
                                },
                            },
                            {
                                "x-tablename": "association",
                                "properties": {
                                    "prop_1": {"x-foreign-key": "foreign.key1"}
                                },
                            },
                        ]
                    },
                )
            ],
            id="single defined",
        ),
        pytest.param(
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association1",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign1.key1"},
                            "prop_2": {"x-foreign-key": "foreign1.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
                types.TNameSchema(
                    name="Association2",
                    schema={
                        "x-tablename": "association2",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign2.key1"},
                            "prop_2": {"x-foreign-key": "foreign2.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
            ],
            {},
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association1",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign1.key1"},
                            "prop_2": {"x-foreign-key": "foreign1.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
                types.TNameSchema(
                    name="Association2",
                    schema={
                        "x-tablename": "association2",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign2.key1"},
                            "prop_2": {"x-foreign-key": "foreign2.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
            ],
            id="multiple not defined",
        ),
        pytest.param(
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association1",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign1.key1"},
                            "prop_2": {"x-foreign-key": "foreign1.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
                types.TNameSchema(
                    name="Association2",
                    schema={
                        "x-tablename": "association2",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign2.key1"},
                            "prop_2": {"x-foreign-key": "foreign2.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
            ],
            {
                "Schema1": {
                    "x-tablename": "association1",
                    "properties": {"prop_1": {"x-foreign-key": "foreign1.key1"}},
                }
            },
            [
                types.TNameSchema(
                    name="Schema1",
                    schema={
                        "allOf": [
                            {
                                "x-tablename": "association1",
                                "properties": {
                                    "prop_2": {"x-foreign-key": "foreign1.key2"},
                                },
                            },
                            {
                                "x-tablename": "association1",
                                "properties": {
                                    "prop_1": {"x-foreign-key": "foreign1.key1"}
                                },
                            },
                        ]
                    },
                ),
                types.TNameSchema(
                    name="Association2",
                    schema={
                        "x-tablename": "association2",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign2.key1"},
                            "prop_2": {"x-foreign-key": "foreign2.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
            ],
            id="multiple first defined",
        ),
        pytest.param(
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association1",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign1.key1"},
                            "prop_2": {"x-foreign-key": "foreign1.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
                types.TNameSchema(
                    name="Association2",
                    schema={
                        "x-tablename": "association2",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign2.key1"},
                            "prop_2": {"x-foreign-key": "foreign2.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
            ],
            {
                "Schema2": {
                    "x-tablename": "association2",
                    "properties": {"prop_1": {"x-foreign-key": "foreign2.key1"}},
                }
            },
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association1",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign1.key1"},
                            "prop_2": {"x-foreign-key": "foreign1.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
                types.TNameSchema(
                    name="Schema2",
                    schema={
                        "allOf": [
                            {
                                "x-tablename": "association2",
                                "properties": {
                                    "prop_2": {"x-foreign-key": "foreign2.key2"},
                                },
                            },
                            {
                                "x-tablename": "association2",
                                "properties": {
                                    "prop_1": {"x-foreign-key": "foreign2.key1"}
                                },
                            },
                        ]
                    },
                ),
            ],
            id="multiple second defined",
        ),
        pytest.param(
            [
                types.TNameSchema(
                    name="Association1",
                    schema={
                        "x-tablename": "association1",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign1.key1"},
                            "prop_2": {"x-foreign-key": "foreign1.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
                types.TNameSchema(
                    name="Association2",
                    schema={
                        "x-tablename": "association2",
                        "properties": {
                            "prop_1": {"x-foreign-key": "foreign2.key1"},
                            "prop_2": {"x-foreign-key": "foreign2.key2"},
                        },
                        "required": ["prop_1", "prop_2"],
                    },
                ),
            ],
            {
                "Schema1": {
                    "x-tablename": "association1",
                    "properties": {"prop_1": {"x-foreign-key": "foreign1.key1"}},
                },
                "Schema2": {
                    "x-tablename": "association2",
                    "properties": {"prop_1": {"x-foreign-key": "foreign2.key1"}},
                },
            },
            [
                types.TNameSchema(
                    name="Schema1",
                    schema={
                        "allOf": [
                            {
                                "x-tablename": "association1",
                                "properties": {
                                    "prop_2": {"x-foreign-key": "foreign1.key2"},
                                },
                            },
                            {
                                "x-tablename": "association1",
                                "properties": {
                                    "prop_1": {"x-foreign-key": "foreign1.key1"}
                                },
                            },
                        ]
                    },
                ),
                types.TNameSchema(
                    name="Schema2",
                    schema={
                        "allOf": [
                            {
                                "x-tablename": "association2",
                                "properties": {
                                    "prop_2": {"x-foreign-key": "foreign2.key2"},
                                },
                            },
                            {
                                "x-tablename": "association2",
                                "properties": {
                                    "prop_1": {"x-foreign-key": "foreign2.key1"}
                                },
                            },
                        ]
                    },
                ),
            ],
            id="multiple all defined",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize("association_schemas, schemas, expected_schemas", TESTS)
    @pytest.mark.schemas
    @pytest.mark.association
    def test_(association_schemas, schemas, expected_schemas):
        """
        GIVEN association_schemas, schemas and expected schemas
        WHEN _combine_defined_expected_schemas is called with the association_schemas
            and schemas
        THEN the expected schemas are returned.
        """
        returned_schemas = association._combine_defined_expected_schemas(
            association_schemas=association_schemas, schemas=schemas
        )

        assert list(returned_schemas) == expected_schemas
