"""Tests for SQLAlchemy simple property facade."""

import functools

import pytest
import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import types
from open_alchemy.facades.sqlalchemy import simple
from open_alchemy.schemas.artifacts import types as artifacts_types


def _create_artifacts():
    """Create column artifacts."""
    return artifacts_types.SimplePropertyArtifacts(
        type=types.PropertyType.SIMPLE,
        open_api=artifacts_types.OpenApiSimplePropertyArtifacts(
            type="integer",
            format=None,
            max_length=None,
            nullable=None,
            default=None,
            read_only=None,
            write_only=None,
        ),
        extension=artifacts_types.ExtensionSimplePropertyArtifacts(
            primary_key=None,
            autoincrement=None,
            index=None,
            unique=None,
            server_default=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
            dict_ignore=None,
        ),
        schema={"type": "integer"},
        required=False,
        description=None,
    )


@pytest.mark.parametrize(
    "type_, expected_type",
    [
        pytest.param("integer", sqlalchemy.Integer, id="integer"),
        pytest.param("number", sqlalchemy.Float, id="number"),
        pytest.param("string", sqlalchemy.String, id="string"),
        pytest.param("boolean", sqlalchemy.Boolean, id="boolean"),
    ],
)
@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct(type_, expected_type):
    """
    GIVEN artifacts for a type
    WHEN construct is called with the artifacts
    THEN a column with the expected type is returned.
    """
    artifacts = _create_artifacts()
    artifacts.open_api.type = type_

    returned_column = simple.construct(artifacts=artifacts)

    assert isinstance(returned_column, sqlalchemy.Column)
    assert isinstance(returned_column.type, expected_type)
    assert len(returned_column.foreign_keys) == 0
    assert returned_column.nullable is True


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_foreign_key():
    """
    GIVEN artifacts with foreign key
    WHEN construct is called with the artifacts
    THEN a column with a foreign key is returned.
    """
    artifacts = _create_artifacts()
    artifacts.extension.foreign_key = "table.column"

    returned_column = simple.construct(artifacts=artifacts)

    assert len(returned_column.foreign_keys) == 1
    foreign_key = returned_column.foreign_keys.pop()
    assert str(foreign_key) == "ForeignKey('table.column')"
    assert foreign_key.name is None


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_foreign_key_kwargs():
    """
    GIVEN artifacts with foreign key and foreign key kwargs
    WHEN construct is called with the artifacts
    THEN a column with a foreign key with the kwargs is returned.
    """
    artifacts = _create_artifacts()
    artifacts.extension.foreign_key = "table.column"
    artifacts.extension.foreign_key_kwargs = {"name": "name 1"}

    returned_column = simple.construct(artifacts=artifacts)

    assert len(returned_column.foreign_keys) == 1
    foreign_key = returned_column.foreign_keys.pop()
    assert foreign_key.name == "name 1"


CONSTRUCT_ARGS_TESTS = [
    pytest.param("open_api", "nullable", True, "nullable", True, id="nullable true"),
    pytest.param("open_api", "nullable", False, "nullable", False, id="nullable false"),
    pytest.param(
        "open_api",
        "default",
        None,
        "nullable",
        True,
        id="default None expect nullable true",
    ),
    pytest.param(
        "open_api",
        "default",
        1,
        "nullable",
        False,
        id="default set expect nullable false",
    ),
    pytest.param(
        "extension",
        "server_default",
        None,
        "nullable",
        True,
        id="server_default None expect nullable true",
    ),
    pytest.param(
        "extension",
        "server_default",
        "value 1",
        "nullable",
        False,
        id="server_default set expect nullable false",
    ),
    pytest.param(
        "extension",
        "server_default",
        None,
        "nullable",
        True,
        id="autoincrement None expect nullable true",
    ),
    pytest.param(
        "extension",
        "autoincrement",
        True,
        "nullable",
        False,
        id="autoincrement set expect nullable false",
    ),
    pytest.param("open_api", "default", None, "default", None, id="default None"),
    pytest.param(
        "open_api", "default", "value 1", "default.arg", "value 1", id="default set"
    ),
    pytest.param(
        "extension",
        "server_default",
        None,
        "server_default",
        None,
        id="server_default None",
    ),
    pytest.param(
        "extension",
        "server_default",
        "value 1",
        "server_default.arg.text",
        "value 1",
        id="server_default set",
    ),
    pytest.param(
        "extension", "primary_key", None, "primary_key", False, id="primary key None"
    ),
    pytest.param(
        "extension", "primary_key", False, "primary_key", False, id="primary key False"
    ),
    pytest.param(
        "extension", "primary_key", True, "primary_key", True, id="primary key True"
    ),
    pytest.param("extension", "index", None, "index", None, id="index None"),
    pytest.param("extension", "index", False, "index", False, id="index False"),
    pytest.param("extension", "index", True, "index", True, id="index True"),
    pytest.param("extension", "unique", None, "unique", None, id="unique None"),
    pytest.param("extension", "unique", False, "unique", False, id="unique False"),
    pytest.param("extension", "unique", True, "unique", True, id="unique True"),
]


@pytest.mark.parametrize(
    "art_parent_key, art_item_key, art_value, column_key, column_value",
    CONSTRUCT_ARGS_TESTS,
)
@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_args(
    art_parent_key, art_item_key, art_value, column_key, column_value
):
    """
    GIVEN artifacts where a key has been set to a value
    WHEN construct is called with the artifacts
    THEN a column where the key has the expected value is returned.
    """
    artifacts = _create_artifacts()
    setattr(getattr(artifacts, art_parent_key), art_item_key, art_value)

    returned_column = simple.construct(artifacts=artifacts)

    assert (
        functools.reduce(getattr, column_key.split("."), returned_column)
        == column_value
    )


@pytest.mark.parametrize(
    "required, expected_nullable",
    [
        pytest.param(False, True, id="required False"),
        pytest.param(True, False, id="required True"),
    ],
)
@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_args_required_nullable(required, expected_nullable):
    """
    GIVEN artifacts with given required
    WHEN construct is called with the artifacts
    THEN a column with the expected nullable value is returned.
    """
    artifacts = _create_artifacts()
    artifacts.required = required

    returned_column = simple.construct(artifacts=artifacts)

    assert returned_column.nullable == expected_nullable


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_default_type_mapped():
    """
    GIVEN artifacts with a format that requires mapping with default value
    WHEN construct is called with the artifacts
    THEN a column with a default value that is mapped is returned.
    """
    artifacts = _create_artifacts()
    artifacts.open_api.type = "string"
    artifacts.open_api.format = "binary"
    artifacts.open_api.default = "value 1"

    returned_column = simple.construct(artifacts=artifacts)

    assert returned_column.default.arg == b"value 1"


@pytest.mark.parametrize(
    "autoincrement, expected_autoincrement",
    [
        pytest.param(None, "auto", id="None"),
        pytest.param(False, False, id="False"),
        pytest.param(True, True, id="True"),
    ],
)
@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_autoincrement(autoincrement, expected_autoincrement):
    """
    GIVEN value for autoincrement
    WHEN construct is called with the artifacts with autoincrement
    THEN the returned column autoincrement property is equal to autoincrement.
    """
    artifacts = _create_artifacts()
    artifacts.open_api.type = "integer"
    artifacts.extension.autoincrement = autoincrement

    returned_column = simple.construct(artifacts=artifacts)

    assert returned_column.autoincrement == expected_autoincrement


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_kwargs():
    """
    GIVEN artifacts with kwargs
    WHEN construct is called with the artifacts
    THEN the column is constructed with the kwargs.
    """
    artifacts = _create_artifacts()
    artifacts.extension.kwargs = {"doc": "doc 1"}

    returned_column = simple.construct(artifacts=artifacts)

    assert returned_column.doc == "doc 1"


class TestDetermineType:
    """Tests for _determine_type."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_unsupported():
        """
        GIVEN artifacts with an unsupported type
        WHEN _determine_type is called with the artifacts
        THEN FeatureNotImplementedError is raised.
        """
        artifacts = _create_artifacts()
        artifacts.open_api.type = "unsupported"

        with pytest.raises(exceptions.FeatureNotImplementedError):
            simple._determine_type(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "type_, expected_type",
        [
            pytest.param("integer", sqlalchemy.Integer, id="integer"),
            pytest.param("number", sqlalchemy.Float, id="number"),
            pytest.param("string", sqlalchemy.String, id="string"),
            pytest.param("boolean", sqlalchemy.Boolean, id="boolean"),
        ],
    )
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_supported(type_, expected_type):
        """
        GIVEN type
        WHEN _determine_type is called with the artifacts with the type
        THEN the expected type is returned.
        """
        artifacts = _create_artifacts()
        artifacts.open_api.type = type_

        returned_type = simple._determine_type(artifacts=artifacts)

        assert isinstance(returned_type, expected_type)


class TestHandleInteger:
    """Tests for _handle_integer."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_invalid_format():
        """
        GIVEN artifacts with format that is not supported
        WHEN _handle_integer is called with the artifacts
        THEN FeatureNotImplementedError is raised.
        """
        artifacts = _create_artifacts()
        artifacts.open_api.type = "integer"
        artifacts.open_api.format = "unsupported"

        with pytest.raises(exceptions.FeatureNotImplementedError):
            simple._handle_integer(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "format_, expected_integer_cls",
        [
            pytest.param(None, sqlalchemy.Integer, id="None"),
            pytest.param("int32", sqlalchemy.Integer, id="int32"),
            pytest.param("int64", sqlalchemy.BigInteger, id="int64"),
        ],
    )
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_valid(format_, expected_integer_cls):
        """
        GIVEN artifacts and expected SQLALchemy type
        WHEN _handle_integer is called with the artifacts
        THEN the expected type is returned.
        """
        artifacts = _create_artifacts()
        artifacts.open_api.type = "integer"
        artifacts.open_api.format = format_

        integer = simple._handle_integer(artifacts=artifacts)

        assert isinstance(integer, expected_integer_cls)


class TestHandleNumber:
    """Tests for _handle_number."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_invalid_format():
        """
        GIVEN artifacts with format that is not supported
        WHEN _handle_number is called with the artifacts
        THEN FeatureNotImplementedError is raised.
        """
        artifacts = _create_artifacts()
        artifacts.open_api.type = "number"
        artifacts.open_api.format = "unsupported"

        with pytest.raises(exceptions.FeatureNotImplementedError):
            simple._handle_number(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "format_, expected_number_cls",
        [
            pytest.param(None, sqlalchemy.Float, id="None"),
            pytest.param("float", sqlalchemy.Float, id="float"),
        ],
    )
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_valid(format_, expected_number_cls):
        """
        GIVEN artifacts and expected SQLALchemy type
        WHEN _handle_integer is called with the artifacts
        THEN the expected type is returned.
        """
        artifacts = _create_artifacts()
        artifacts.open_api.type = "number"
        artifacts.open_api.format = format_

        number = simple._handle_number(artifacts=artifacts)

        assert isinstance(number, expected_number_cls)


class TestHandleString:
    """Tests for _handle_string."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "format_, expected_type",
        [
            pytest.param(
                None,
                sqlalchemy.String,
                id="None",
            ),
            pytest.param(
                "date",
                sqlalchemy.Date,
                id="date",
            ),
            pytest.param(
                "date-time",
                sqlalchemy.DateTime,
                id="date-time",
            ),
            pytest.param(
                "byte",
                sqlalchemy.String,
                id="byte",
            ),
            pytest.param(
                "password",
                sqlalchemy.String,
                id="password",
            ),
            pytest.param("binary", sqlalchemy.LargeBinary, id="binary"),
            pytest.param("unsupported", sqlalchemy.String, id="unsupported"),
        ],
    )
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_valid(format_, expected_type):
        """
        GIVEN artifacts and expected SQLALchemy type
        WHEN _handle_string is called with the artifacts
        THEN the expected type is returned.
        """
        artifacts = _create_artifacts()
        artifacts.open_api.type = "string"
        artifacts.open_api.format = format_

        string = simple._handle_string(artifacts=artifacts)

        assert isinstance(string, expected_type)

    @staticmethod
    @pytest.mark.parametrize(
        "format_, expected_type",
        [
            pytest.param(None, sqlalchemy.String, id="string"),
            pytest.param("binary", sqlalchemy.LargeBinary, id="binary"),
        ],
    )
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_valid_max_length(format_, expected_type):
        """
        GIVEN artifacts with max_length and given format
        WHEN _handle_string is called with the artifacts
        THEN a given expected type column with a maximum length is returned.
        """
        length = 1
        artifacts = _create_artifacts()
        artifacts.open_api.type = "string"
        artifacts.open_api.format = format_
        artifacts.open_api.max_length = length

        string = simple._handle_string(artifacts=artifacts)

        assert isinstance(string, expected_type)
        assert string.length == length


class TestHandleBoolean:
    """Tests for _handle_boolean."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    @pytest.mark.sqlalchemy
    def test_valid():
        """
        GIVEN
        WHEN _handle_boolean is called
        THEN the boolean type is returned.
        """
        boolean = simple._handle_boolean()

        assert isinstance(boolean, sqlalchemy.Boolean)
