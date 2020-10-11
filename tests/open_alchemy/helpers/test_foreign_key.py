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
            relationship.Type.MANY_TO_ONE,
            {
                "allOf": [
                    {"x-foreign-key-column": "name_1"},
                    {"$ref": "#/components/schemas/RefSchema"},
                ]
            },
            {"RefSchema": {"x-foreign-key-column": "name_2"}},
            "name_1",
            id="many-to-one defined overridden first",
        ),
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "name_1"},
                ]
            },
            {"RefSchema": {"x-foreign-key-column": "name_2"}},
            "name_1",
            id="many-to-one defined overridden second",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-uselist": False}},
            "id",
            id="one-to-one not defined",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-foreign-key-column": "name", "x-uselist": False}},
            "name",
            id="one-to-one defined",
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
        type_=type_, property_schema=schema, schemas=schemas
    )

    assert returned_name == expected_column_name


@pytest.mark.parametrize(
    "type_, parent_schema, property_schema, schemas, expected_schema",
    [
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"parent_key": "parent value"},
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"ref_key": "ref value"}},
            {"ref_key": "ref value"},
            id="one-to-many",
        ),
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"parent_key": "parent value"},
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"ref_key": "ref value"}},
            {"ref_key": "ref value"},
            id="one-to-many allOf",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            {"parent_key": "parent value"},
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"ref_key": "ref value"}},
            {"ref_key": "ref value"},
            id="one-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"parent_key": "parent value"},
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"ref_key": "ref value"}},
            {"parent_key": "parent value"},
            id="many-to-one",
        ),
    ],
)
@pytest.mark.helper
def test_get_target_schema(
    type_, parent_schema, property_schema, schemas, expected_schema
):
    """
    GIVEN relationship type, parent and property schema, schemas and expected schema
    WHEN get_target_schema is called with the type, parent and property schema and
        schemas
    THEN the expected schema is returned.
    """
    returned_schema = foreign_key.get_target_schema(
        type_=type_,
        parent_schema=parent_schema,
        property_schema=property_schema,
        schemas=schemas,
    )

    assert returned_schema == expected_schema


@pytest.mark.parametrize(
    "type_, column_name, property_name, schema, schemas, expected_prop_name",
    [
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            "column_1",
            "prop_1",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            "prop_1_column_1",
            id="many-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            "column_1",
            "prop_1",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-uselist": False}},
            "prop_1_column_1",
            id="one-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            "column_1",
            "prop_1",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-tablename": "ref_schema"}},
            "ref_schema_prop_1_column_1",
            id="one-to-many",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            "column_1",
            "prop_1",
            {
                "allOf": [
                    {"x-inherits": True, "x-tablename": "child_table"},
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            {"ParentSchema": {"x-tablename": "parent_schema"}},
            "child_table_prop_1_column_1",
            id="one-to-many joined table child first",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            "column_1",
            "prop_1",
            {
                "allOf": [
                    {"$ref": "#/components/schemas/ParentSchema"},
                    {"x-inherits": True, "x-tablename": "child_table"},
                ]
            },
            {"ParentSchema": {"x-tablename": "parent_schema"}},
            "child_table_prop_1_column_1",
            id="one-to-many joined table child first",
        ),
    ],
)
@pytest.mark.helper
def test_calculate_prop_name(
    type_, column_name, property_name, schema, schemas, expected_prop_name
):
    """
    GIVEN relationship type, schema, schemas and expected prop name
    WHEN calculate_prop_name is called with the type, schema and schemas
    THEN the expected foreign key prop name is returned.
    """
    returned_name = foreign_key.calculate_prop_name(
        type_=type_,
        column_name=column_name,
        property_name=property_name,
        target_schema=schema,
        schemas=schemas,
    )

    assert returned_name == expected_prop_name


@pytest.mark.parametrize(
    "target_schema, schemas, expected_key",
    [
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-tablename": "table_1"}},
            "table_1.fk_column",
            id="plain",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-inherits": True, "x-tablename": "child_table"},
                    {"$ref": "#/components/schemas/RefSchema"},
                ]
            },
            {"RefSchema": {"x-tablename": "parent_table"}},
            "child_table.fk_column",
            id="joined table child first",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-inherits": True, "x-tablename": "child_table"},
                ]
            },
            {"RefSchema": {"x-tablename": "parent_table"}},
            "child_table.fk_column",
            id="joined table child last",
        ),
    ],
)
@pytest.mark.helper
def test_calculate_foreign_key(target_schema, schemas, expected_key):
    """
    GIVEN the target schema and foreign key column name and the expected key
    WHEN calculate_foreign_key is called with target schema and foreign key column name
    THEN the expected foreign key is returned.
    """

    returned_key = foreign_key.calculate_foreign_key(
        column_name="fk_column",
        target_schema=target_schema,
        schemas=schemas,
    )

    assert returned_key == expected_key


@pytest.mark.parametrize(
    "type_, parent_schema, property_schema, schemas, expected_schema",
    [
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            {"parent_key": "parent value"},
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"ref_key": "ref value"}},
            {"parent_key": "parent value"},
            id="many-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            {"parent_key": "parent value"},
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"ref_key": "ref value"}},
            {"parent_key": "parent value"},
            id="one-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            {"parent_key": "parent value"},
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"ref_key": "ref value"}},
            {"ref_key": "ref value"},
            id="one-to-many",
        ),
    ],
)
@pytest.mark.helper
def test_get_modify_schema(
    type_, parent_schema, property_schema, schemas, expected_schema
):
    """
    GIVEN relationship type, parent and property schema, schemas and expected schema
    WHEN get_modify_schema is called with the type, parent and property schema and
        schemas
    THEN the expected schema is returned.
    """
    returned_schema = foreign_key.get_modify_schema(
        type_=type_,
        parent_schema=parent_schema,
        property_schema=property_schema,
        schemas=schemas,
    )

    assert returned_schema == expected_schema


@pytest.mark.parametrize(
    "type_, parent_name, property_schema, schemas, expected_schema",
    [
        pytest.param(
            relationship.Type.MANY_TO_ONE,
            "ParentSchema",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"ref_key": "ref value"}},
            "ParentSchema",
            id="one-to-many",
        ),
        pytest.param(
            relationship.Type.ONE_TO_ONE,
            "ParentSchema",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"ref_key": "ref value"}},
            "ParentSchema",
            id="one-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            "ParentSchema",
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"ref_key": "ref value"}},
            "RefSchema",
            id="many-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            "ParentSchema",
            {"allOf": [{"items": {"$ref": "#/components/schemas/RefSchema"}}]},
            {"RefSchema": {"ref_key": "ref value"}},
            "RefSchema",
            id="allOf many-to-one",
        ),
        pytest.param(
            relationship.Type.ONE_TO_MANY,
            "ParentSchema",
            {"items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}},
            {"RefSchema": {"ref_key": "ref value"}},
            "RefSchema",
            id="many-to-one allOf",
        ),
    ],
)
@pytest.mark.helper
def test_get_modify_name(type_, parent_name, property_schema, schemas, expected_schema):
    """
    GIVEN relationship type, parent name, property schema, schemas and expected name
    WHEN get_modify_name is called with the type, parent name, property schema and
        schemas
    THEN the expected name is returned.
    """
    returned_schema = foreign_key.get_modify_name(
        type_=type_,
        parent_name=parent_name,
        property_schema=property_schema,
        schemas=schemas,
    )

    assert returned_schema == expected_schema
