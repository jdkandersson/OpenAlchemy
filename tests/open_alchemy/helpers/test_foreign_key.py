"""Tests for foreign key helper."""

import pytest

from open_alchemy.helpers import foreign_key
from open_alchemy.helpers import relationship


@pytest.mark.parametrize(
    "type_, schema, schemas, expected_column_name",
    [
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            "id",
            id="many-to-one not defined",
        ),
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-foreign-key-column": "name"}},
            "name",
            id="many-to-one defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
            "id",
            id="one-to-many not defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"x-foreign-key-column": "name"}},
            "name",
            id="one-to-many defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"allOf": [{"items": {"$ref": "#/components/schemas/RefSchema"}}]},
            {"RefSchema": {"x-foreign-key-column": "name"}},
            "name",
            id="allOf one-to-many defined",
        ),
    ],
)
@pytest.mark.helper
def test_calculate_column_name(type_, schema, schemas, expected_column_name):
    """
    GIVEN relationship type, schema, schemas and expected column name
    WHEN calculate_column_name is called with the type, schema and schemas
    THEN the expected foreign key column name is returned.
    """
    returned_name = foreign_key.calculate_column_name(
        type_=type_, schema=schema, schemas=schemas
    )

    assert returned_name == expected_column_name


@pytest.mark.helper
def test_calculate_prop_name_x_to_one():
    """
    GIVEN the property name and foreign key column name
    WHEN calculate_prop_name_x_to_one is called with property name and foreign key
        column name
    THEN the expected foreign key property name is returned.
    """
    returned_name = foreign_key.calculate_prop_name_x_to_one(
        property_name="property_1", foreign_key_column_name="fk_column"
    )

    assert returned_name == "property_1_fk_column"


@pytest.mark.helper
def test_calculate_prop_name_one_to_many():
    """
    GIVEN the tablename, property name and foreign key column name
    WHEN calculate_prop_name_one_to_many is called with tablename, property name and
        foreign key column name
    THEN the expected foreign key property name is returned.
    """
    returned_name = foreign_key.calculate_prop_name_one_to_many(
        tablename="table_1",
        property_name="property_1",
        foreign_key_column_name="fk_column",
    )

    assert returned_name == "table_1_property_1_fk_column"


@pytest.mark.helper
def test_calculate_foreign_key():
    """
    GIVEN the tablename and foreign key column name
    WHEN calculate_foreign_key is called with tablename and foreign key
        column name
    THEN the expected foreign key is returned.
    """
    returned_key = foreign_key.calculate_foreign_key(
        tablename="table_1", foreign_key_column_name="fk_column"
    )

    assert returned_key == "table_1.fk_column"
