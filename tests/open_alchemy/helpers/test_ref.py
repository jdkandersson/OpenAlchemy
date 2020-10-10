"""Tests for ref."""

import os
from unittest import mock
from urllib import error

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


@pytest.mark.parametrize(
    "schema, schemas, expected_name",
    [
        ({"type": "integer"}, {}, "Schema"),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "integer"}},
            "RefSchema",
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {"$ref": "#/components/schemas/NestedRefSchema"},
                "NestedRefSchema": {"type": "integer"},
            },
            "NestedRefSchema",
        ),
    ],
    ids=["no $ref", "single $ref", "nested $ref"],
)
@pytest.mark.helper
def test_resolve_valid(schema, schemas, expected_name):
    """
    GIVEN schema, schemas and expected name
    WHEN resolve is called with the schema, schemas and name
    THEN the schema and expected name are returned.
    """
    name = "Schema"

    (return_name, return_schema) = helpers.ref.resolve(
        name=name, schema=schema, schemas=schemas
    )

    assert return_name == expected_name
    assert return_schema == {"type": "integer"}


@pytest.mark.parametrize(
    "schema, schemas, expected_name, expected_schema",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"key": "value"}},
            "Schema",
            {},
        ),
        (
            {"$ref": "#/components/schemas/IntermediateSchema"},
            {
                "IntermediateSchema": {"$ref": "#/components/schemas/RefSchema"},
                "RefSchema": {"key": "value"},
            },
            "IntermediateSchema",
            {},
        ),
        (
            {"$ref": "#/components/schemas/OtherSchema"},
            {"OtherSchema": {"key": "value"}},
            "OtherSchema",
            {"key": "value"},
        ),
    ],
    ids=["skip hit", "nested skip hit", "skip miss"],
)
@pytest.mark.helper
def test_resolve_valid_skip(schema, schemas, expected_name, expected_schema):
    """
    GIVEN schema, schemas and schema name to skip
    WHEN resolve is called with the schema, schemas, name and schema to skip
    THEN an empty schema is returned.
    """
    name = "Schema"
    skip_name = "RefSchema"

    (return_name, return_schema) = helpers.ref.resolve(
        name=name, schema=schema, schemas=schemas, skip_name=skip_name
    )

    assert return_name == expected_name
    assert return_schema == expected_schema


@pytest.mark.parametrize(
    "schema, schemas, exception",
    [
        pytest.param(
            {"$ref": True}, {}, exceptions.MalformedSchemaError, id="$ref not string"
        ),
        pytest.param(
            {"$ref": "#/components/not/schema"},
            {},
            exceptions.SchemaNotFoundError,
            id="invalid $ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {},
            exceptions.SchemaNotFoundError,
            id="not defined",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"$ref": "#/components/schemas/RefSchema"}},
            exceptions.MalformedSchemaError,
            id="single step circular reference",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {"$ref": "#/components/schemas/NestedRefSchema"},
                "NestedRefSchema": {"$ref": "#/components/schemas/RefSchema"},
            },
            exceptions.MalformedSchemaError,
            id="multiple step circular reference",
        ),
    ],
)
@pytest.mark.helper
def test_resolve_error(schema, schemas, exception):
    """
    GIVEN schema and schemas that are not valid
    WHEN resolve is called with the schema
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        helpers.ref.resolve(name="name 1", schema=schema, schemas=schemas)


@pytest.mark.parametrize(
    "context, expected_context",
    [
        (os.path.join("dir", "doc.ext"), os.path.join("dir", "doc.ext")),
        (os.path.join("dir", "..", "doc.ext"), "doc.ext"),
        ("http://host.com/doc.ext", "http://host.com/doc.ext"),
    ],
    ids=["no norm", "norm", "URL"],
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


class TestSeperateContextPath:
    """Tests for _add_remote_context."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.helper
    def test_invalid():
        """
        GIVEN ref without #
        WHEN _separate_context_path is called with the ref
        THEN MalformedSchemaError is raised.
        """
        with pytest.raises(exceptions.MalformedSchemaError):
            helpers.ref._separate_context_path(ref="invalid")

    @staticmethod
    @pytest.mark.parametrize(
        "ref, expected_context, expected_path",
        [("#/Schema1", "", "/Schema1"), ("Context1#/Schema1", "Context1", "/Schema1")],
        ids=["no context", "with context"],
    )
    @pytest.mark.helper
    def test_valid(ref, expected_context, expected_path):
        """
        GIVEN valid ref
        WHEN _separate_context_path is called with the ref
        THEN the expected context and path is returned.
        """
        context, path = helpers.ref._separate_context_path(ref=ref)

        assert context == expected_context
        assert path == expected_path


class TestAddRemoteContext:
    """Tests for _add_remote_context."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "context, ref, exp_exception",
        [
            ("", "", exceptions.MalformedSchemaError),
            ("", "context1#context2#doc1.ext", exceptions.MalformedSchemaError),
            ("doc.ext", "//some.server#Schema1", exceptions.SchemaNotFoundError),
        ],
        ids=["# missing", "multiple #", "// without URL context"],
    )
    @pytest.mark.helper
    def test_error(context, ref, exp_exception):
        """
        GIVEN invalid context or ref
        WHEN _add_remote_context is called with the context and ref
        THEN the given expected exception is raised.
        """
        with pytest.raises(exp_exception):
            helpers.ref._add_remote_context(context=context, ref=ref)

    @staticmethod
    @pytest.mark.parametrize(
        "context, ref, expected_ref",
        [
            pytest.param(
                "doc1.ext",
                "#/Schema",
                "doc1.ext#/Schema",
                id="within document context document",
            ),
            pytest.param(
                "dir1/doc1.ext",
                "#/Schema",
                # Not with os.path.join because context has folder
                "dir1/doc1.ext#/Schema",
                id="within document context folder",
            ),
            pytest.param(
                "doc1.ext",
                "doc2.ext#/Schema",
                "doc2.ext#/Schema",
                id="external same folder context document",
            ),
            pytest.param(
                "dir1/doc1.ext",
                "doc2.ext#/Schema",
                os.path.join("dir1", "doc2.ext#/Schema"),
                id="external same folder context folder",
            ),
            pytest.param(
                "doc1.ext",
                "dir2/doc2.ext#/Schema",
                os.path.join("dir2", "doc2.ext#/Schema"),
                id="external different folder context document",
            ),
            pytest.param(
                "dir1/doc1.ext",
                "dir2/doc2.ext#/Schema",
                os.path.join("dir1", "dir2", "doc2.ext#/Schema"),
                id="external different folder context folder",
            ),
            pytest.param(
                "doc1.ext",
                "dir2/../doc2.ext#/Schema",
                "doc2.ext#/Schema",
                id="external different folder require normalization context document",
            ),
            pytest.param(
                "dir1/doc1.ext",
                "../doc2.ext#/Schema",
                "doc2.ext#/Schema",
                id="external different folder require normalization context folder",
            ),
            pytest.param(
                "http://host.com/doc1.ext",
                "#/Schema",
                "http://host.com/doc1.ext#/Schema",
                id="http within document context document",
            ),
            pytest.param(
                "http://host.com/dir1/doc1.ext",
                "#/Schema",
                "http://host.com/dir1/doc1.ext#/Schema",
                id="http within document context folder",
            ),
            pytest.param(
                "HTTP://host.com/doc1.ext",
                "#/Schema",
                "HTTP://host.com/doc1.ext#/Schema",
                id="http capitalized context document",
            ),
            pytest.param(
                "https://host.com/doc1.ext",
                "#/Schema",
                "https://host.com/doc1.ext#/Schema",
                id="https context document",
            ),
            pytest.param(
                "HTTPS://host.com/doc1.ext",
                "#/Schema",
                "HTTPS://host.com/doc1.ext#/Schema",
                id="https capitalized context document",
            ),
            pytest.param(
                "http://host.com/doc1.ext",
                "doc2.ext#/Schema",
                "http://host.com/doc2.ext#/Schema",
                id="http same folder context document",
            ),
            pytest.param(
                "http://host.com/dir1/doc1.ext",
                "doc2.ext#/Schema",
                "http://host.com/dir1/doc2.ext#/Schema",
                id="http same folder context folder",
            ),
            pytest.param(
                "http://host.com/doc1.ext",
                "dir2/doc2.ext#/Schema",
                "http://host.com/dir2/doc2.ext#/Schema",
                id="http different folder context document",
            ),
            pytest.param(
                "http://host.com/dir1/doc1.ext",
                "dir2/doc2.ext#/Schema",
                "http://host.com/dir1/dir2/doc2.ext#/Schema",
                id="http different folder context folder",
            ),
            pytest.param(
                "http://host.com/doc1.ext",
                "dir2/../doc2.ext#/Schema",
                "http://host.com/doc2.ext#/Schema",
                id="http different folder require normalization context document",
            ),
            pytest.param(
                "http://host.com/dir1/doc1.ext",
                "../doc2.ext#/Schema",
                "http://host.com/doc2.ext#/Schema",
                id="http different folder require normalization context folder",
            ),
            pytest.param(
                "http://host1.com/doc1.ext",
                "http://host2.com/doc1.ext#/Schema",
                "http://host2.com/doc1.ext#/Schema",
                id="http other http context document",
            ),
            pytest.param(
                "http://host1.com/doc1.ext",
                "HTTP://host2.com/doc1.ext#/Schema",
                "HTTP://host2.com/doc1.ext#/Schema",
                id="http other http capitalized context document",
            ),
            pytest.param(
                "http://host1.com/doc1.ext",
                "https://host2.com/doc1.ext#/Schema",
                "https://host2.com/doc1.ext#/Schema",
                id="http other https context document",
            ),
            pytest.param(
                "http://host1.com/doc1.ext",
                "HTTPS://host2.com/doc1.ext#/Schema",
                "HTTPS://host2.com/doc1.ext#/Schema",
                id="http other https capitalized context document",
            ),
            pytest.param(
                "http://host1.com/doc1.ext",
                "//host2.com/doc1.ext#/Schema",
                "http://host2.com/doc1.ext#/Schema",
                id="http other network no protocol context document",
            ),
            pytest.param(
                "doc1.ext",
                "http://host.com/doc1.ext#/Schema",
                "http://host.com/doc1.ext#/Schema",
                id="within document to http context document",
            ),
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
    @pytest.mark.helper
    def test_init():
        """
        GIVEN
        WHEN _RemoteSchemaStore is initialized
        THEN empty store is created.
        """
        store = helpers.ref._RemoteSchemaStore()

        assert store._schemas == {}
        assert store.spec_context is None

    @staticmethod
    @pytest.mark.helper
    def test_reset():
        """
        GIVEN store which has a spec path and schemas
        WHEN reset is called
        THEN the state is removed.
        """
        store = helpers.ref._RemoteSchemaStore()
        store._schemas["key"] = "value"
        store.spec_context = "path 1"

        store.reset()

        assert store._schemas == {}
        assert store.spec_context is None

    @staticmethod
    @pytest.mark.helper
    def test_context_not_set():
        """
        GIVEN _RemoteSchemaStore without spec context set
        WHEN get_schemas is called
        THEN MissingArgumentError is raised.
        """
        store = helpers.ref._RemoteSchemaStore()

        with pytest.raises(exceptions.MissingArgumentError):
            store.get_schemas(context="doc.ext")

    @staticmethod
    @pytest.mark.parametrize(
        "context", ["dir1/.dir2/", "doc.ext"], ids=["not a file", "not json nor yaml"]
    )
    @pytest.mark.helper
    def test_invalid_extension(context):
        """
        GIVEN context with invalid extension
        WHEN get_schemas is called
        THEN SchemaNotFoundError is raised.
        """
        store = helpers.ref._RemoteSchemaStore()
        store.spec_context = "doc.ext"

        with pytest.raises(exceptions.SchemaNotFoundError):
            store.get_schemas(context=context)

    @staticmethod
    @pytest.mark.helper
    def test_file_not_found(tmp_path):
        """
        GIVEN path to a file that doesn't exist
        WHEN get_schemas is called with the path as the context
        THEN SchemaNotFoundError is raised.
        """
        # Create file
        directory = tmp_path / "base"
        directory.mkdir()
        schemas_file = directory / "original.json"
        # Create store
        store = helpers.ref._RemoteSchemaStore()
        store.spec_context = str(schemas_file)

        with pytest.raises(exceptions.SchemaNotFoundError):
            store.get_schemas(context="remote.json")

    @staticmethod
    @pytest.mark.parametrize(
        "remote_context, contents",
        [("remote.json", "not: valid: JSON"), ("remote.yaml", "not: valid: YAML")],
        ids=["invalid JSON", "invalid YAML"],
    )
    @pytest.mark.helper
    def test_invalid_contents(tmp_path, remote_context, contents):
        """
        GIVEN file with invalid contents
        WHEN get_schemas is called with the path to the file
        THEN SchemaNotFoundError is raised.
        """
        # Create file
        directory = tmp_path / "base"
        directory.mkdir()
        schemas_file = directory / "original.json"
        remote_schemas_file = directory / remote_context
        remote_schemas_file.write_text(contents)
        # Create store
        store = helpers.ref._RemoteSchemaStore()
        store.spec_context = str(schemas_file)

        with pytest.raises(exceptions.SchemaNotFoundError):
            store.get_schemas(context=remote_context)

    @staticmethod
    @pytest.mark.parametrize(
        "remote_context, contents",
        [
            ("remote.json", '{"key": "value"}'),
            ("remote.JSON", '{"key": "value"}'),
            ("remote.yaml", "key: value"),
            ("remote.YAML", "key: value"),
            ("remote.yml", "key: value"),
        ],
        ids=[".json", ".JSON", ".yaml", ".YAML", ".yml"],
    )
    @pytest.mark.helper
    def test_load_success(tmp_path, remote_context, contents):
        """
        GIVEN file with schemas
        WHEN get_schemas is called with the path to the file
        THEN the loaded contents are returned.
        """
        # Create file
        directory = tmp_path / "base"
        directory.mkdir()
        schemas_file = directory / "original.json"
        remote_schemas_file = directory / remote_context
        remote_schemas_file.write_text(contents)
        # Create store
        store = helpers.ref._RemoteSchemaStore()
        store.spec_context = str(schemas_file)

        remote_schemas = store.get_schemas(context=remote_context)

        assert remote_schemas == {"key": "value"}

    @staticmethod
    @pytest.mark.helper
    def test_load_twice(tmp_path):
        """
        GIVEN file with schemas
        WHEN get_schemas is called with the path to the file, it is deleted and then
            get_schemas is called again
        THEN the loaded JSON contents are returned.
        """
        # Create file
        directory = tmp_path / "base"
        directory.mkdir()
        schemas_file = directory / "original.json"
        remote_schemas_file = directory / "remote.json"
        remote_schemas_file.write_text('{"key": "value"}')
        # Create store
        store = helpers.ref._RemoteSchemaStore()
        store.spec_context = str(schemas_file)

        store.get_schemas(context="remote.json")
        os.remove(str(remote_schemas_file))
        remote_schemas = store.get_schemas(context="remote.json")

        assert remote_schemas == {"key": "value"}

    @staticmethod
    @pytest.mark.helper
    def test_load_different_directory(tmp_path):
        """
        GIVEN file with schemas in a different directory
        WHEN get_schemas is called with the path to the file
        THEN the loaded JSON contents are returned.
        """
        # Create file
        directory = tmp_path / "base"
        directory.mkdir()
        schemas_file = directory / "original.json"
        remote_directory = directory / "remote"
        remote_directory.mkdir()
        remote_schemas_file = remote_directory / "remote.json"
        remote_schemas_file.write_text('{"key": "value"}')
        # Create store
        store = helpers.ref._RemoteSchemaStore()
        store.spec_context = str(schemas_file)

        remote_schemas = store.get_schemas(context="remote/remote.json")

        assert remote_schemas == {"key": "value"}

    @staticmethod
    @pytest.mark.helper
    def test_load_url_success(mocked_urlopen):
        """
        GIVEN context with HTTP path
        WHEN get_schemas is called with the path to the file
        THEN the loaded contents are returned.
        """
        # Defining returned data
        response_cm = mock.MagicMock()
        response_cm.getcode.return_value = 200
        response_cm.read.return_value = '{"key": "value"}'
        response_cm.__enter__.return_value = response_cm
        mocked_urlopen.return_value = response_cm
        # Create store
        store = helpers.ref._RemoteSchemaStore()
        store.spec_context = "path1"
        remote_context = "http://host.com/doc.json"

        remote_schemas = store.get_schemas(context=remote_context)

        assert remote_schemas == {"key": "value"}

    @staticmethod
    @pytest.mark.helper
    def test_load_url_error(mocked_urlopen):
        """
        GIVEN loading file from a URL fails
        WHEN get_schemas is called with the path to the file
        THEN SchemaNotFoundError is raised.
        """
        # Defining urlopen raising error
        mocked_urlopen.side_effect = error.HTTPError(
            url="some url", code=404, msg="message", hdrs="headers", fp="fp"
        )
        # Create store
        store = helpers.ref._RemoteSchemaStore()
        store.spec_context = "path1"
        remote_context = "http://host.com/doc.json"

        with pytest.raises(exceptions.SchemaNotFoundError):
            store.get_schemas(context=remote_context)


class TestRetrieveSchema:
    """Tests for _retrieve_schema."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schemas, path",
        [
            ({"Schema1": {"key1": "value1"}}, "/Schema2"),
            ({"Parent1": {"Schema1": {"key1": "value1"}}}, "/Parent2/Schema1"),
        ],
        ids=["root", "single level"],
    )
    @pytest.mark.helper
    def test_miss(schemas, path):
        """
        GIVEN schemas and path where the path doesn't resolve
        WHEN _retrieve_schema is called with the schemas and path
        THEN SchemaNotFoundError is raised.
        """
        with pytest.raises(exceptions.SchemaNotFoundError):
            helpers.ref._retrieve_schema(schemas=schemas, path=path)

    @staticmethod
    @pytest.mark.parametrize(
        "schemas, path",
        [
            ({"Schema1": {"key1": "value1"}}, "/Schema1"),
            ({"Parent": {"Schema1": {"key1": "value1"}}}, "/Parent/Schema1"),
            (
                {"Grandparent": {"Parent": {"Schema1": {"key1": "value1"}}}},
                "/Grandparent/Parent/Schema1",
            ),
            (
                {"Schema1": {"key1": "value1"}, "Schema2": {"key2": "value2"}},
                "/Schema1",
            ),
        ],
        ids=["root", "single level", "multiple levels", "with siblings"],
    )
    @pytest.mark.helper
    def test_valid(schemas, path):
        """
        GIVEN schemas and path to schema
        WHEN _retrieve_schema is called with the schemas and path
        THEN the schema at the path is returned.
        """
        name, schema = helpers.ref._retrieve_schema(schemas=schemas, path=path)

        assert schema == {"key1": "value1"}
        assert name == "Schema1"


@pytest.mark.helper
def test_get_remote_ref(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN remote $ref and file with the remote schemas
    WHEN get_remote_ref is called with the $ref
    THEN the remote schema is returned.
    """
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text('{"Schema1": {"key": "value"}}')
    # Set up remote schemas store
    helpers.ref.set_context(path=str(schemas_file))
    # Calculate $ref
    ref = "remote.json#/Schema1"

    name, schema = helpers.ref.get_remote_ref(ref=ref)

    assert schema == {"key": "value"}
    assert name == "Schema1"


@pytest.mark.helper
def test_get_remote_ref_norm(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN remote $ref that is not normalized and file with the remote schemas
    WHEN get_remote_ref is called with the $ref
    THEN the schemas are stored under the normalized path.
    """
    # pylint: disable=protected-access
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    sub_directory = directory / "subdir"
    sub_directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text('{"Schema1": {"key": "value"}}')
    # Set up remote schemas store
    helpers.ref.set_context(path=str(schemas_file))
    # Calculate $ref
    ref = "subdir/../remote.json#/Schema1"

    helpers.ref.get_remote_ref(ref=ref)

    assert "remote.json" in helpers.ref._remote_schema_store._schemas


@pytest.mark.helper
def test_get_remote_ref_ref(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN remote $ref and file with the remote schemas
    WHEN get_remote_ref is called with the $ref
    THEN the remote schema is returned.
    """
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text('{"Schema1": {"$ref": "#/Schema2"}}')
    # Set up remote schemas store
    helpers.ref.set_context(path=str(schemas_file))
    # Calculate $ref
    ref = "remote.json#/Schema1"

    name, schema = helpers.ref.get_remote_ref(ref=ref)

    assert schema == {"$ref": "remote.json#/Schema2"}
    assert name == "Schema1"


@pytest.mark.helper
def test_get_remote_ref_remote_ref(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN remote $ref and file with the remote schemas
    WHEN get_remote_ref is called with the $ref
    THEN the remote schema is returned.
    """
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text(
        '{"Schema1": {"$ref": "dir1/other_remote.json#/Schema2"}}'
    )
    # Set up remote schemas store
    helpers.ref.set_context(path=str(schemas_file))
    # Calculate $ref
    ref = "remote.json#/Schema1"

    name, schema = helpers.ref.get_remote_ref(ref=ref)

    assert schema == {"$ref": "dir1/other_remote.json#/Schema2"}
    assert name == "Schema1"


@pytest.mark.helper
def test_resolve_remote(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN remote $ref and file with the remote schemas
    WHEN resolve is called with the $ref
    THEN the remote schema is returned.
    """
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text('{"Schema1": {"key": "value"}}')
    # Set up remote schemas store
    helpers.ref.set_context(path=str(schemas_file))
    # Calculate $ref
    schema = {"$ref": "remote.json#/Schema1"}

    returned_name, returned_schema = helpers.ref.resolve(
        name="name 1", schema=schema, schemas={}
    )

    assert returned_schema == {"key": "value"}
    assert returned_name == "Schema1"


@pytest.mark.helper
def test_resolve_remote_url(mocked_urlopen, _clean_remote_schemas_store):
    """
    GIVEN remote $ref and urlopen with the remote schemas
    WHEN resolve is called with the $ref
    THEN the remote schema is returned.
    """
    # Defining returned data
    response_cm = mock.MagicMock()
    response_cm.getcode.return_value = 200
    response_cm.read.return_value = '{"Schema1": {"key": "value"}}'
    response_cm.__enter__.return_value = response_cm
    mocked_urlopen.return_value = response_cm
    # Set up remote schemas store
    helpers.ref.set_context(path="path1")
    # Calculate $ref
    schema = {"$ref": "http://host.com/remote.json#/Schema1"}

    returned_name, returned_schema = helpers.ref.resolve(
        name="name 1", schema=schema, schemas={}
    )

    assert returned_schema == {"key": "value"}
    assert returned_name == "Schema1"


@pytest.mark.helper
def test_set_spec_context(_clean_remote_schemas_store):
    """
    GIVEN spec context
    WHEN set_spec_context is called
    THEN the RemoteSchemaStore has the context.
    """
    # pylint: disable=protected-access

    helpers.ref.set_context(path="path1")

    assert helpers.ref._remote_schema_store.spec_context == "path1"
