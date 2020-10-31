"""Tests for _check_properties_valid function in association validation."""

import pytest

from open_alchemy import types
from open_alchemy.schemas import helpers
from open_alchemy.schemas import validation


class TestCheckPropertiesValid:
    """Tests for _check_properties_valid."""

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
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "wrong foreign key",
                    }
                }
            },
            {},
            False,
            (
                "unexpected",
                "foreign key",
                '"wrong foreign key"',
                '"prop_1"',
                '"parent_table.parent_column"',
                '"ref_table.ref_column"',
            ),
            id="single property unexpected foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "parent_table.parent_column",
                        "type": "wrong type",
                        "format": "parent format",
                        "maxLength": 1,
                    }
                }
            },
            {},
            False,
            (
                "unexpected",
                "type",
                '"prop_1"',
                '"wrong type"',
                '"parent type"',
            ),
            id="single property parent wrong type",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "parent_table.parent_column",
                        "type": "parent type",
                        "format": "wrong format",
                        "maxLength": 1,
                    }
                }
            },
            {},
            False,
            (
                "unexpected",
                "format",
                '"prop_1"',
                '"wrong format"',
                '"parent format"',
            ),
            id="single property parent wrong format",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "parent_table.parent_column",
                        "type": "parent type",
                        "format": "parent format",
                        "maxLength": 2,
                    }
                }
            },
            {},
            False,
            (
                "unexpected",
                "maxLength",
                '"prop_1"',
                '"2"',
                '"1"',
            ),
            id="single property parent wrong maxLength",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "parent_table.parent_column",
                        "type": "parent type",
                        "format": "parent format",
                        "maxLength": 1,
                    }
                }
            },
            {},
            True,
            None,
            id="single property parent valid",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "allOf": [
                            {
                                "x-primary-key": True,
                                "x-foreign-key": "parent_table.parent_column",
                                "type": "parent type",
                                "format": "parent format",
                                "maxLength": 1,
                            },
                            {"$ref": "#/components/schemas/RefProperty"},
                        ]
                    }
                }
            },
            {"RefProperty": {"x-foreign-key": "wrong foreign key"}},
            True,
            None,
            id="single property parent valid foreign key local ref local first",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "allOf": [
                            {"$ref": "#/components/schemas/RefProperty"},
                            {
                                "x-primary-key": True,
                                "x-foreign-key": "parent_table.parent_column",
                                "type": "parent type",
                                "format": "parent format",
                                "maxLength": 1,
                            },
                        ]
                    }
                }
            },
            {"RefProperty": {"x-foreign-key": "wrong foreign key"}},
            True,
            None,
            id="single property parent valid foreign key local ref ref first",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "ref_table.ref_column",
                        "type": "wrong type",
                    }
                }
            },
            {},
            False,
            (
                "unexpected",
                "type",
                '"prop_1"',
                '"wrong type"',
                '"ref type"',
            ),
            id="single property ref wrong type",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "parent_table.parent_column",
                        "type": "parent type",
                        "format": "parent format",
                    },
                    "prop_2": {
                        "x-primary-key": True,
                        "x-foreign-key": "ref_table.ref_column",
                        "type": "ref type",
                    },
                }
            },
            {},
            False,
            ("prop_1",),
            id="multiple property first wrong",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "parent_table.parent_column",
                        "type": "parent type",
                        "format": "parent format",
                        "maxLength": 1,
                    },
                    "prop_2": {
                        "x-primary-key": True,
                        "x-foreign-key": "ref_table.ref_column",
                        "type": "wrong type",
                    },
                }
            },
            {},
            False,
            ("prop_2",),
            id="multiple property second wrong",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "parent_table.parent_column",
                        "type": "parent type",
                        "format": "parent format",
                        "maxLength": 1,
                    },
                    "prop_2": {
                        "x-primary-key": True,
                        "x-foreign-key": "ref_table.ref_column",
                        "type": "ref type",
                    },
                }
            },
            {},
            True,
            None,
            id="multiple property valid",
        ),
    ]

    @staticmethod
    @pytest.mark.schemas
    @pytest.mark.validate
    @pytest.mark.parametrize("schema, schemas, expected_valid, expected_reasons", TESTS)
    def test_(schema, schemas, expected_valid, expected_reasons):
        """
        GIVEN schema, schemas, and expected valid and reasons
        WHEN _check_properties_valid is called with the schema and schemas
        THEN the expected valid and reasons are returned.
        """
        name = "Schema"
        association = helpers.association.TParentPropertySchema(
            parent=types.TNameSchema(
                name="ParentSchema",
                schema={
                    "x-tablename": "parent_table",
                    "properties": {
                        "parent_column": {
                            "type": "parent type",
                            "x-primary-key": True,
                            "format": "parent format",
                            "maxLength": 1,
                        }
                    },
                },
            ),
            property=types.TNameSchema(
                name="PropertySchema",
                schema={"items": {"$ref": "#/components/schemas/RefSchema"}},
            ),
        )
        schemas["RefSchema"] = {
            "x-tablename": "ref_table",
            "x-secondary": "association",
            "properties": {"ref_column": {"type": "ref type", "x-primary-key": True}},
        }

        returned_result = validation.association._check_properties_valid(
            name=name, schema=schema, association=association, schemas=schemas
        )

        assert returned_result.valid == expected_valid
        if expected_reasons is not None:
            expected_reasons = (
                *expected_reasons,
                name,
                association.parent.name,
                association.property.name,
            )

            for reason in expected_reasons:
                assert reason in returned_result.reason
