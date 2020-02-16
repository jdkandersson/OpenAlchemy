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
