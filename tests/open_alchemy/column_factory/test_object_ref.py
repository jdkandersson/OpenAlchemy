"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy.column_factory import object_ref


@pytest.mark.parametrize(
    "spec, schemas",
    [
        ({"type": "object"}, {}),
        ({"allOf": [{"type": "object"}]}, {}),
        (
            {"$ref": "#/components/schemas/Schema"},
            {
                "Schema": {
                    "type": "object",
                    "x-tablename": "table",
                    "x-secondary": "secondary",
                }
            },
        ),
    ],
    ids=["object", "allOf with object", "secondary defined"],
)
@pytest.mark.column
def test_handle_object_error(spec, schemas):
    """
    GIVEN spec
    WHEN handle_object is called with the spec
    THEN MalformedRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedRelationshipError):
        object_ref.handle_object(
            spec=spec,
            schemas=schemas,
            required=True,
            logical_name="name 1",
            model_schema={},
        )


@pytest.mark.parametrize(
    "spec",
    [
        [{"type": "object"}],
        [{"$ref": "ref 1"}, {"$ref": "ref 2"}],
        [{"$ref": "ref 1"}, {"x-backref": "backref 1"}, {"x-backref": "backref 2"}],
        [
            {"$ref": "ref 1"},
            {"x-secondary": "secondary 1"},
            {"x-secondary": "secondary 2"},
        ],
        [
            {"$ref": "ref 1"},
            {"x-foreign-key-column": "column 1"},
            {"x-foreign-key-column": "column 2"},
        ],
        [{"$ref": "ref 1"}, {"x-uselist": True}, {"x-uselist": False}],
    ],
    ids=[
        "object",
        "multiple ref",
        "multiple x-backref",
        "multiple x-secondary",
        "multiple x-foreign-key-column",
        "multiple x-uselist",
    ],
)
@pytest.mark.column
def test_check_object_all_of_error(spec):
    """
    GIVEN spec
    WHEN _check_object_all_of is called with the spec
    THEN MalformedRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedRelationshipError):
        object_ref._check_object_all_of(all_of_spec=spec)


@pytest.mark.parametrize(
    "spec, schemas, fk_column",
    [
        ({"properties": {"id": {}}}, {}, "id"),
        ({"x-tablename": "table 1"}, {}, "id"),
        ({"x-tablename": "table 1", "properties": {}}, {}, "id"),
        (
            {"x-tablename": "table 1", "properties": {"id": {"type": "integer"}}},
            {},
            "column_1",
        ),
        ({"x-tablename": "table 1", "properties": {"id": {}}}, {}, "id"),
    ],
    ids=[
        "no tablename",
        "no properties",
        "no id property",
        "custom foreign key property missing",
        "id property no type",
    ],
)
@pytest.mark.column
def test_handle_object_reference_malformed_schema(spec, schemas, fk_column):
    """
    GIVEN spec, schemas and foreign key column
    WHEN handle_object_reference is called with the spec, schemas and foreign key
        column
    THEN a MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        object_ref.handle_object_reference(
            spec=spec, schemas=schemas, fk_column=fk_column
        )


@pytest.mark.column
def test_handle_object_reference_fk_return():
    """
    GIVEN foreign key column and object schema with x-tablename and id and foreign key
        property with a type
    WHEN handle_object_reference is called with the schema
    THEN a schema with the type of the foreign key property and x-foreign-key property.
    """
    spec = {
        "x-tablename": "table 1",
        "properties": {"id": {"type": "idType"}, "fk": {"type": "fkType"}},
    }
    schemas = {}

    return_value = object_ref.handle_object_reference(
        spec=spec, schemas=schemas, fk_column="fk"
    )

    assert return_value == {"type": "fkType", "x-foreign-key": "table 1.fk"}


@pytest.mark.parametrize(
    "spec, schemas, expected_spec",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            {"type": "object"},
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"type": "object"}]}},
            {"type": "object"},
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            {"type": "object"},
        ),
    ],
    ids=["$ref", "$ref to allOf", "allOf"],
)
@pytest.mark.column
def test_gather_object_artifacts_spec(spec, schemas, expected_spec):
    """
    GIVEN specification, schemas and expected specification
    WHEN gather_object_artifacts is called with the specification and schemas
    THEN the expected specification is returned.
    """
    obj_artifacts = object_ref.gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert obj_artifacts.spec == expected_spec


@pytest.mark.parametrize(
    "spec, schemas",
    [
        ({"$ref": "#/components/schemas/RefSchema"}, {"RefSchema": {"type": "object"}}),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
        ),
    ],
    ids=["$ref", "allOf"],
)
@pytest.mark.column
def test_gather_object_artifacts_ref_logical_name(spec, schemas):
    """
    GIVEN specification and schemas
    WHEN gather_object_artifacts is called with the specification and schemas
    THEN the referenced schema name is returned as the ref logical name.
    """
    obj_artifacts = object_ref.gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert obj_artifacts.ref_logical_name == "RefSchema"


@pytest.mark.parametrize(
    "spec, schemas, expected_backref",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "x-backref": "backref 1"}},
            "backref 1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "backref 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                    {"x-uselist": False},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "backref 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "backref 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2", "x-uselist": False},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "backref 2",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object", "x-backref": "backref 1"}},
            "backref 1",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object", "x-backref": "backref 1"}},
            "backref 2",
        ),
    ],
    ids=[
        "$ref no backref",
        "$ref backref",
        "allOf no backref",
        "allOf backref",
        "allOf backref before other",
        "allOf backref after other",
        "allOf backref with uselist",
        "allOf $ref backref",
        "allOf backref $ref backref",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_backref(spec, schemas, expected_backref):
    """
    GIVEN specification and schemas and expected backref
    WHEN gather_object_artifacts is called with the specification and schemas
    THEN the expected backref is returned.
    """
    obj_artifacts = object_ref.gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert obj_artifacts.backref == expected_backref


@pytest.mark.column
def test_gather_object_artifacts_uselist_no_backref():
    """
    GIVEN specification with uselist but not backref and schemas
    WHEN gather_object_artifacts is called with the specification and schemas
    THEN MalformedRelationshipError is raised.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {"RefSchema": {"type": "object", "x-uselist": False}}

    with pytest.raises(exceptions.MalformedRelationshipError):
        object_ref.gather_object_artifacts(spec=spec, logical_name="", schemas=schemas)


@pytest.mark.parametrize(
    "spec, schemas, expected_uselist",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "type": "object",
                    "x-backref": "backref 1",
                    "x-uselist": True,
                }
            },
            True,
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            False,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False, "x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            False,
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {
                "RefSchema": {
                    "type": "object",
                    "x-backref": "backref 1",
                    "x-uselist": True,
                }
            },
            True,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                    {"x-uselist": False},
                ]
            },
            {
                "RefSchema": {
                    "type": "object",
                    "x-backref": "backref 1",
                    "x-uselist": True,
                }
            },
            False,
        ),
    ],
    ids=[
        "$ref no uselist",
        "$ref uselist",
        "allOf no uselist",
        "allOf uselist",
        "allOf uselist with backref",
        "allOf $ref uselist",
        "allOf uselist $ref uselist",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_uselist(spec, schemas, expected_uselist):
    """
    GIVEN specification and schemas and expected uselist
    WHEN gather_object_artifacts is called with the specification and schemas
    THEN the expected uselist is returned.
    """
    obj_artifacts = object_ref.gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert obj_artifacts.uselist == expected_uselist


@pytest.mark.parametrize(
    "spec, schemas, expected_secondary",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "x-secondary": "secondary 1"}},
            "secondary 1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "secondary 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "secondary 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "secondary 2"},
                    {"x-backref": "backref 1"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "secondary 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 1"},
                    {"x-secondary": "secondary 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "secondary 2",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object", "x-secondary": "secondary 1"}},
            "secondary 1",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "secondary 2"},
                ]
            },
            {"RefSchema": {"type": "object", "x-secondary": "secondary 1"}},
            "secondary 2",
        ),
    ],
    ids=[
        "$ref no secondary",
        "$ref secondary",
        "allOf no secondary",
        "allOf secondary",
        "allOf secondary before other",
        "allOf secondary after other",
        "allOf $ref secondary",
        "allOf secondary $ref secondary",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_secondary(spec, schemas, expected_secondary):
    """
    GIVEN specification and schemas and expected secondary
    WHEN gather_object_artifacts is called with the specification and schemas
    THEN the expected secondary is returned.
    """
    obj_artifacts = object_ref.gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert obj_artifacts.secondary == expected_secondary


@pytest.mark.parametrize(
    "spec, schemas, expected_fk_column",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            "id",
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "x-foreign-key-column": "fk_column_1"}},
            "fk_column_1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            "id",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "fk_column_2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "fk_column_2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "fk_column_2"},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "fk_column_2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                    {"x-foreign-key-column": "fk_column_2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "fk_column_2",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object", "x-foreign-key-column": "fk_column_1"}},
            "fk_column_1",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "fk_column_2"},
                ]
            },
            {"RefSchema": {"type": "object", "x-foreign-key-column": "fk_column_1"}},
            "fk_column_2",
        ),
    ],
    ids=[
        "$ref no fk",
        "$ref fk",
        "allOf no fk",
        "allOf fk",
        "allOf fk before other",
        "allOf fk after other",
        "allOf $ref fk",
        "allOf fk $ref fk",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_fk_column(spec, schemas, expected_fk_column):
    """
    GIVEN specification and schemas and expected foreign key column
    WHEN gather_object_artifacts is called with the specification and schemas
    THEN the expected foreign key column is returned.
    """
    obj_artifacts = object_ref.gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert obj_artifacts.fk_column == expected_fk_column


@pytest.mark.parametrize(
    "model_schema",
    [
        {
            "properties": {
                "ref_table_fk_column": {"x-foreign-key": "ref_table.fk_column"}
            }
        },
        {
            "properties": {
                "ref_table_fk_column": {
                    "type": "not_fk_type",
                    "x-foreign-key": "ref_table.fk_column",
                }
            }
        },
        {"properties": {"ref_table_fk_column": {"type": "fk_type"}}},
        {
            "properties": {
                "ref_table_fk_column": {
                    "type": "fk_type",
                    "x-foreign-key": "wrong_table.wrong_column",
                }
            }
        },
    ],
    ids=["no type", "wrong type", "no x-foreign-key", "wrong x-foreign-key"],
)
@pytest.mark.column
def test_check_foreign_key_required_invalid_schema(model_schema):
    """
    GIVEN model schema that is not valid
    WHEN check_foreign_key_required is called
    THEN MalformedRelationshipError is raised.
    """
    fk_spec = {"type": "fk_type", "x-foreign-key": "ref_table.fk_column"}
    fk_logical_name = "ref_table_fk_column"

    with pytest.raises(exceptions.MalformedRelationshipError):
        object_ref.check_foreign_key_required(
            fk_spec=fk_spec,
            fk_logical_name=fk_logical_name,
            model_schema=model_schema,
            schemas={},
        )


@pytest.mark.parametrize(
    "model_schema, schemas, expected_required",
    [
        ({"properties": {}}, {}, True),
        (
            {
                "properties": {
                    "ref_table_fk_column": {
                        "type": "fk_type",
                        "x-foreign-key": "ref_table.fk_column",
                    }
                }
            },
            {},
            False,
        ),
        (
            {
                "properties": {
                    "ref_table_fk_column": {"$ref": "#/components/schemas/FkSchema"}
                }
            },
            {"FkSchema": {"type": "fk_type", "x-foreign-key": "ref_table.fk_column"}},
            False,
        ),
        (
            {
                "properties": {
                    "ref_table_fk_column": {
                        "allOf": [
                            {"type": "fk_type", "x-foreign-key": "ref_table.fk_column"}
                        ]
                    }
                }
            },
            {},
            False,
        ),
    ],
    ids=[
        "not in model schema",
        "in model schema",
        "in model schema $ref",
        "in model schema allOf",
    ],
)
@pytest.mark.column
def test_check_foreign_key_required(model_schema, schemas, expected_required):
    """
    GIVEN foreign key spec, foreign key logical name, model schema, schemas and
        expected required
    WHEN check_foreign_key_required is called
    THEN the expected required is returned.
    """
    fk_spec = {"type": "fk_type", "x-foreign-key": "ref_table.fk_column"}
    fk_logical_name = "ref_table_fk_column"

    required = object_ref.check_foreign_key_required(
        fk_spec=fk_spec,
        fk_logical_name=fk_logical_name,
        model_schema=model_schema,
        schemas=schemas,
    )

    assert required == expected_required
