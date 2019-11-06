"""Tests for the column factory."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy.column_factory import object_ref


@pytest.mark.parametrize(
    "spec",
    [{"type": "object"}, {"allOf": [{"type": "object"}]}],
    ids=["object", "allOf with object"],
)
@pytest.mark.column
def test_handle_object_error(spec):
    """
    GIVEN spec
    WHEN handle_object is called with the spec
    THEN MalformedManyToOneRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedManyToOneRelationshipError):
        object_ref.handle_object(
            spec=spec, schemas={"type": "object"}, required=True, logical_name="name 1"
        )


@pytest.mark.parametrize(
    "spec",
    [
        [{"type": "object"}],
        [{"$ref": "ref 1"}, {"$ref": "ref 2"}],
        [{"$ref": "ref 1"}, {"x-backref": "backref 1"}, {"x-backref": "backref 2"}],
        [
            {"$ref": "ref 1"},
            {"x-foreign-key-column": "column 1"},
            {"x-foreign-key-column": "column 2"},
        ],
    ],
    ids=[
        "object",
        "multiple ref",
        "multiple x-backref",
        "multiple x-foreign-key-column",
    ],
)
@pytest.mark.column
def test_check_object_all_of_error(spec):
    """
    GIVEN spec
    WHEN handle_object is called with the spec
    THEN MalformedManyToOneRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedManyToOneRelationshipError):
        object_ref._check_object_all_of(all_of_spec=spec)


@pytest.mark.column
def test_handle_object_reference_no_tablename():
    """
    GIVEN object schema without x-tablename key
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        object_ref._handle_object_reference(
            spec={"properties": {"id": {}}}, schemas={}, fk_column="id"
        )


@pytest.mark.column
def test_handle_object_reference_no_properties():
    """
    GIVEN object schema without properties key
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        object_ref._handle_object_reference(
            spec={"x-tablename": "table 1"}, schemas={}, fk_column="id"
        )


@pytest.mark.column
def test_handle_object_reference_id_missing():
    """
    GIVEN object schema without id in properties
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        object_ref._handle_object_reference(
            spec={"x-tablename": "table 1", "properties": {}},
            schemas={},
            fk_column="id",
        )


@pytest.mark.column
def test_handle_object_reference_name_missing():
    """
    GIVEN foreign key argument and object schema without foreign key property
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        object_ref._handle_object_reference(
            spec={"x-tablename": "table 1", "properties": {"id": {"type": "integer"}}},
            schemas={},
            fk_column="column_1",
        )


@pytest.mark.column
def test_handle_object_reference_id_no_type():
    """
    GIVEN object schema with id but no type for id
    WHEN _handle_object_reference is called with the schema
    THEN a MalformedSchemaError should be raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        object_ref._handle_object_reference(
            spec={"x-tablename": "table 1", "properties": {"id": {}}},
            schemas={},
            fk_column="id",
        )


@pytest.mark.column
def test_handle_object_reference_fk_return():
    """
    GIVEN foreign key column and object schema with x-tablename and id and foreign key
        property with a type
    WHEN _handle_object_reference is called with the schema
    THEN a schema with the type of the foreign key property and x-foreign-key property.
    """
    spec = {
        "x-tablename": "table 1",
        "properties": {"id": {"type": "idType"}, "fk": {"type": "fkType"}},
    }
    schemas = {}

    return_value = object_ref._handle_object_reference(
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
def test_gather_object_artifacts_spec(spec, schemas, expected_spec):
    """
    GIVEN specification, schemas and expected specification
    WHEN _gather_object_artifacts is called with the specification and schemas
    THEN the expected specification is returned.
    """
    returned_spec, _, _, _ = object_ref._gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert returned_spec == expected_spec


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
def test_gather_object_artifacts_ref_logical_name(spec, schemas):
    """
    GIVEN specification and schemas
    WHEN _gather_object_artifacts is called with the specification and schemas
    THEN the referenced schema name is returned as the ref logical name.
    """
    _, ref_logical_name, _, _ = object_ref._gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert ref_logical_name == "RefSchema"


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
        "allOf $ref backref",
        "allOf backref $ref backref",
    ],
)
def test_gather_object_artifacts_backref(spec, schemas, expected_backref):
    """
    GIVEN specification and schemas and expected backref
    WHEN _gather_object_artifacts is called with the specification and schemas
    THEN the expected backref is returned.
    """
    _, _, backref, _ = object_ref._gather_object_artifacts(
        spec=spec, logical_name="", schemas=schemas
    )

    assert backref == expected_backref
