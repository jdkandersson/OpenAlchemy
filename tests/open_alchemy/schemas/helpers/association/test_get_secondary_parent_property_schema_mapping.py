"""Tests for the get_secondary_parent_property_schema_mapping association helper."""

import pytest

from open_alchemy.schemas.helpers import association

TESTS = [
    pytest.param(
        {},
        {},
        id="empty",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "schema",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        {},
        id="single schema single property not association",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "schema",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                },
            },
            "RefSchema": {"x-secondary": "association"},
        },
        {
            "association": (
                (
                    "Schema",
                    {
                        "x-tablename": "schema",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        },
                    },
                ),
                (
                    "prop_1",
                    {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            )
        },
        id="single schema single association",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "schema",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema1"},
                    },
                    "prop_2": {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema2"},
                    },
                },
            },
            "RefSchema1": {"x-secondary": "association_1"},
            "RefSchema2": {"x-secondary": "association_2"},
        },
        {
            "association_1": (
                (
                    "Schema",
                    {
                        "x-tablename": "schema",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "key_1": "value 1",
                                "items": {"$ref": "#/components/schemas/RefSchema1"},
                            },
                            "prop_2": {
                                "type": "array",
                                "key_2": "value 2",
                                "items": {"$ref": "#/components/schemas/RefSchema2"},
                            },
                        },
                    },
                ),
                (
                    "prop_1",
                    {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema1"},
                    },
                ),
            ),
            "association_2": (
                (
                    "Schema",
                    {
                        "x-tablename": "schema",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "key_1": "value 1",
                                "items": {"$ref": "#/components/schemas/RefSchema1"},
                            },
                            "prop_2": {
                                "type": "array",
                                "key_2": "value 2",
                                "items": {"$ref": "#/components/schemas/RefSchema2"},
                            },
                        },
                    },
                ),
                (
                    "prop_2",
                    {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema2"},
                    },
                ),
            ),
        },
        id="single schema multiple association",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema1"},
                    }
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema2"},
                    }
                },
            },
            "RefSchema1": {"x-secondary": "association_1"},
            "RefSchema2": {"x-secondary": "association_2"},
        },
        {
            "association_1": (
                (
                    "Schema1",
                    {
                        "x-tablename": "schema_1",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "key_1": "value 1",
                                "items": {"$ref": "#/components/schemas/RefSchema1"},
                            }
                        },
                    },
                ),
                (
                    "prop_1",
                    {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema1"},
                    },
                ),
            ),
            "association_2": (
                (
                    "Schema2",
                    {
                        "x-tablename": "schema_2",
                        "properties": {
                            "prop_2": {
                                "type": "array",
                                "key_2": "value 2",
                                "items": {"$ref": "#/components/schemas/RefSchema2"},
                            }
                        },
                    },
                ),
                (
                    "prop_2",
                    {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema2"},
                    },
                ),
            ),
        },
        id="multiple schema single association",
    ),
]


@pytest.mark.parametrize("schemas, expected_mapping", TESTS)
@pytest.mark.schemas
@pytest.mark.helper
def test_(schemas, expected_mapping):
    """
    GIVEN schemas and expected mapping
    WHEN get_secondary_parent_property_schema_mapping is called with the schemas
    THEN the expected mapping are returned.
    """
    returned_mapping = association.get_secondary_parent_property_schema_mapping(
        schemas=schemas
    )

    assert returned_mapping == expected_mapping
