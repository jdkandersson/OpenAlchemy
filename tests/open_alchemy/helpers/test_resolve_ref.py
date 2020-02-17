"""Tests for ref."""

import copy

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.helper
def test_ref_resolve_exists():
    """
    GIVEN
    WHEN
    THEN helpers has ref_resolve property.
    """
    assert hasattr(helpers.ref, "resolve")


@pytest.mark.helper
def test_resolve_not_ref_schema():
    """
    GIVEN schema that does not have $ref and name
    WHEN resolve is called with the schema and name
    THEN the schema and name are returned.
    """
    name = "name 1"
    schema = {"type": "integer"}
    schemas = {}

    (return_name, return_schema) = helpers.ref.resolve(
        name=name, schema=copy.deepcopy(schema), schemas=schemas
    )

    assert return_name == name
    assert return_schema == schema


@pytest.mark.helper
def test_resolve_not_schema():
    """
    GIVEN schema that references something that is not a schema
    WHEN resolve is called with the schema
    THEN SchemaNotFoundError is raised.
    """
    schema = {"$ref": "#/components/not/schema"}
    schemas = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        helpers.ref.resolve(name="name 1", schema=schema, schemas=schemas)


@pytest.mark.helper
def test_resolve_not_defined():
    """
    GIVEN schema that references a schema that doesn't exist
    WHEN resolve is called with the schema
    THEN SchemaNotFoundError is raised.
    """
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        helpers.ref.resolve(name="name 1", schema=schema, schemas=schemas)


@pytest.mark.helper
def test_resolve_single():
    """
    GIVEN schema that references another schema and schemas
    WHEN resolve is called with the schema and schemas
    THEN the referenced schema and logical name is returned.
    """
    ref_schema = {"type": "boolean"}
    ref_name = "RefSchema"
    schema = {"$ref": f"#/components/schemas/{ref_name}"}
    schemas = {ref_name: copy.deepcopy(ref_schema)}

    (return_name, return_schema) = helpers.ref.resolve(
        name="name 1", schema=schema, schemas=schemas
    )

    assert return_name == ref_name
    assert return_schema == ref_schema


@pytest.mark.helper
def test_resolve_nested():
    """
    GIVEN schema that references another schema which also references another schema
        and schemas
    WHEN resolve is called with the schema and schemas
    THEN the final referenced schema and logical name is returned.
    """
    ref_schema = {"type": "boolean"}
    ref_name = "RefSchema"
    schema = {"$ref": "#/components/schemas/NestedRefSchema"}
    schemas = {
        "NestedRefSchema": {"$ref": f"#/components/schemas/{ref_name}"},
        "RefSchema": copy.deepcopy(ref_schema),
    }

    (return_name, return_schema) = helpers.ref.resolve(
        name="name 1", schema=schema, schemas=schemas
    )

    assert return_name == ref_name
    assert return_schema == ref_schema


@pytest.mark.parametrize(
    "context, expected_context",
    [("dir/doc.ext", "dir/doc.ext"), ("dir/../doc.ext", "doc.ext")],
    ids=["no norm", "norm"],
)
@pytest.mark.helper
def test_norm_context(context, expected_context):
    """
    GIVEN context
    WHEN _norm_context is called with the context
    THEN the expected context is returned.
    """
    # pylint: disable=protected-access
    returned_context = helpers.ref._norm_context(context=context)

    assert returned_context == expected_context


class TestAddRemoteContext:
    """Tests for _add_remote_context."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "context, ref",
        [("", ""), ("", "context1#context2#doc1.ext")],
        ids=["# missing", "multiple #"],
    )
    @pytest.mark.helper
    def test_error(context, ref):
        """
        GIVEN invalid context or ref
        WHEN _add_remote_context is called with the context and ref
        THEN MalformedSchemaError is raised.
        """
        with pytest.raises(exceptions.MalformedSchemaError):
            helpers.ref._add_remote_context(context=context, ref=ref)

    @staticmethod
    @pytest.mark.parametrize(
        "context, ref, expected_ref",
        [
            ("doc1.ext", "#/Schema", "doc1.ext#/Schema"),
            ("dir1/doc1.ext", "#/Schema", "dir1/doc1.ext#/Schema"),
            ("doc1.ext", "doc2.ext#/Schema", "doc2.ext#/Schema"),
            ("dir1/doc1.ext", "doc2.ext#/Schema", "dir1/doc2.ext#/Schema"),
            ("doc1.ext", "dir2/doc2.ext#/Schema", "dir2/doc2.ext#/Schema"),
            ("dir1/doc1.ext", "dir2/doc2.ext#/Schema", "dir1/dir2/doc2.ext#/Schema"),
            ("doc1.ext", "dir2/../doc2.ext#/Schema", "doc2.ext#/Schema"),
            ("dir1/doc1.ext", "../doc2.ext#/Schema", "doc2.ext#/Schema"),
        ],
        ids=[
            "within document                                 context document",
            "                                                context folder",
            "external same folder                            context document",
            "                                                context folder",
            "external different folder                       context document",
            "                                                context folder",
            "external different folder require normalization context document",
            "                                                context folder",
        ],
    )
    @pytest.mark.helper
    def test_add_remote_context(context, ref, expected_ref):
        """
        GIVEN context and value of a reference
        WHEN _add_remote_context is called with the context and value
        THEN the expected reference value is returned.
        """
        returned_ref = helpers.ref._add_remote_context(context=context, ref=ref)

        assert returned_ref == expected_ref


@pytest.mark.parametrize(
    "schema, expected_schema",
    [
        ({}, {}),
        ({"$ref": "#/Schema1"}, {"$ref": "doc.ext#/Schema1"}),
        (
            {"key1": {"$ref": "#/Schema1"}, "key2": {"$ref": "#/Schema2"}},
            {
                "key1": {"$ref": "doc.ext#/Schema1"},
                "key2": {"$ref": "doc.ext#/Schema2"},
            },
        ),
    ],
    ids=["no update", "single update", "multiple update"],
)
@pytest.mark.helper
def test_map_remote_schema_ref(schema, expected_schema):
    """
    GIVEN schema and context
    WHEN _map_remote_schema_ref is called with the schema and context
    THEN the expected schema is returned.
    """
    # pylint: disable=protected-access
    context = "doc.ext"

    returned_schema = helpers.ref._map_remote_schema_ref(schema=schema, context=context)

    assert returned_schema == expected_schema


class TestRemoteSchemaStore:
    """Tests for _RemoteSchemaStore."""

    # pylint: disable=protected-access

    @staticmethod
    def test_init():
        """
        GIVEN
        WHEN _RemoteSchemaStore is initialized
        THEN empty store is created.
        """
        store = helpers.ref._RemoteSchemaStore()

        assert store._schemas == {}
        assert store.spec_path is None

    @staticmethod
    def test_reset():
        """
        GIVEN store which has a spec path and schemas
        WHEN reset is called
        THEN the state is removed.
        """
        store = helpers.ref._RemoteSchemaStore()
        store._schemas["key"] = "value"
        store.spec_path = "path 1"

        store.reset()

        assert store._schemas == {}
        assert store.spec_path is None
