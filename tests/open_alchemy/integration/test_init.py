"""Integration tests for initialization."""

import json
import sys
from unittest import mock

import pytest
import yaml

import open_alchemy
from open_alchemy import facades


@pytest.mark.integration
def test_init_optional_base_none_call(
    mocked_init_model_factory: mock.MagicMock, mocked_declarative_base: mock.MagicMock
):
    """
    GIVEN mocked init_model_factory and declarative_base
    WHEN _init_optional_base is called with none base
    THEN init_model_factory is called with declarative_base return value as base.
    """
    # pylint: disable=protected-access
    spec = mock.MagicMock()

    open_alchemy._init_optional_base(base=None, spec=spec, define_all=True)

    mocked_init_model_factory.assert_called_once_with(
        base=mocked_declarative_base.return_value,
        spec=spec,
        define_all=True,
        models_filename=None,
        spec_path=None,
    )


@pytest.mark.integration
def test_init_optional_base_none_return(
    _mocked_init_model_factory: mock.MagicMock, mocked_declarative_base: mock.MagicMock
):
    """
    GIVEN mocked init_model_factory and declarative_base
    WHEN _init_optional_base is called with none base
    THEN the declarative_base return value is returned as base.
    """
    # pylint: disable=protected-access
    spec = mock.MagicMock()

    base, _ = open_alchemy._init_optional_base(base=None, spec=spec, define_all=True)

    assert base == mocked_declarative_base.return_value


@pytest.mark.integration
def test_init_optional_base_def_call(mocked_init_model_factory: mock.MagicMock):
    """
    GIVEN mocked init_model_factory and mock base
    WHEN _init_optional_base is called with the base
    THEN init_model_factory is called with base.
    """
    # pylint: disable=protected-access
    spec = mock.MagicMock()
    base = mock.MagicMock()

    open_alchemy._init_optional_base(base=base, spec=spec, define_all=True)

    mocked_init_model_factory.assert_called_once_with(
        base=base, spec=spec, define_all=True, models_filename=None, spec_path=None
    )


@pytest.mark.integration
def test_init_optional_base_def_return(_mocked_init_model_factory: mock.MagicMock):
    """
    GIVEN mocked init_model_factory and and mock base
    WHEN _init_optional_base is called with the base
    THEN the base is returned.
    """
    # pylint: disable=protected-access
    spec = mock.MagicMock()
    base = mock.MagicMock()

    returned_base, _ = open_alchemy._init_optional_base(
        base=base, spec=spec, define_all=True
    )

    assert returned_base == base


@pytest.mark.integration
def test_empty_spec():
    """
    GIVEN empty specification
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(open_alchemy.exceptions.MalformedSpecificationError):
        open_alchemy.init_model_factory(base=None, spec={})


@pytest.mark.integration
def test_empty_components():
    """
    GIVEN specification with empty components
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(open_alchemy.exceptions.MalformedSpecificationError):
        open_alchemy.init_model_factory(base=None, spec={"components": {}})


@pytest.mark.integration
def test_cache_diff(mocked_model_factory: mock.MagicMock):
    """
    GIVEN valid specification and mocked model_factory
    WHEN return value of init_model_factory is called with different names
    THEN mocked model_factory is called the same number of times the return value is
        called.
    """
    model_factory = open_alchemy.init_model_factory(
        base=mock.MagicMock,
        spec={
            "components": {
                "schemas": {
                    "Schema1": {
                        "x-tablename": "schema_1",
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                }
            }
        },
    )

    model_factory(name="table 1")
    model_factory(name="table 2")

    assert mocked_model_factory.call_count == 2


@pytest.mark.integration
def test_cache_same(mocked_model_factory: mock.MagicMock):
    """
    GIVEN valid specification and mocked model_factory
    WHEN return value of init_model_factory is called multiple times with the same name
    THEN mocked model_factory is called once.
    """
    model_factory = open_alchemy.init_model_factory(
        base=mock.MagicMock,
        spec={
            "components": {
                "schemas": {
                    "Schema1": {
                        "x-tablename": "schema_1",
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                }
            }
        },
    )

    model_factory(name="table 1")
    model_factory(name="table 1")

    assert mocked_model_factory.call_count == 1


@pytest.mark.integration
def test_schema():
    """
    GIVEN valid specification with single property
    WHEN return value of init_model_factory is called with the name of the schema
    THEN a SQLAlchemy model with a single property is returned.
    """
    model_factory = open_alchemy.init_model_factory(
        base=mock.MagicMock,
        spec={
            "components": {
                "schemas": {
                    "Table": {
                        "properties": {"column": {"type": "integer"}},
                        "x-tablename": "table",
                        "type": "object",
                    }
                }
            }
        },
    )

    model = model_factory(name="Table")

    # Checking model
    assert model.__tablename__ == "table"
    assert hasattr(model, "column")
    assert isinstance(model.column.type, facades.sqlalchemy.column.Integer)


BASIC_SPEC = {
    "components": {
        "schemas": {
            "Table": {
                "properties": {"column": {"type": "integer", "x-primary-key": True}},
                "x-tablename": "table",
                "type": "object",
            }
        }
    }
}


@pytest.mark.integration
def test_init_json(engine, sessionmaker, tmp_path):
    """
    GIVEN specification stored in a JSON file
    WHEN init_json is called with the file
    THEN a valid model factory is returned.
    """
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.json"
    spec_file.write_text(json.dumps(BASIC_SPEC))

    # Creating model factory
    base, model_factory = open_alchemy.init_json(str(spec_file), define_all=False)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    value = 0
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value


@pytest.mark.integration
def test_init_json_remote(engine, sessionmaker, tmp_path, _clean_remote_schemas_store):
    """
    GIVEN specification stored in a JSON file with a remote reference to another JSON
        file
    WHEN init_json is called with the file
    THEN a valid model factory is returned.
    """
    # Defining specification
    base_spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {"column": {"$ref": "remote_spec.json#/Column"}},
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    remote_spec = {"Column": {"type": "integer", "x-primary-key": True}}

    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.json"
    spec_file.write_text(json.dumps(base_spec))
    remote_spec_file = directory / "remote_spec.json"
    remote_spec_file.write_text(json.dumps(remote_spec))

    # Creating model factory
    base, model_factory = open_alchemy.init_json(str(spec_file), define_all=False)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    value = 0
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value


@pytest.mark.integration
def test_init_yaml(engine, sessionmaker, tmp_path):
    """
    GIVEN specification stored in a YAML file
    WHEN init_yaml is called with the file
    THEN a valid model factory is returned.
    """
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(BASIC_SPEC))

    # Creating model factory
    base, model_factory = open_alchemy.init_yaml(str(spec_file), define_all=False)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    value = 0
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value


@pytest.mark.integration
def test_init_yaml_remote(engine, sessionmaker, tmp_path, _clean_remote_schemas_store):
    """
    GIVEN specification stored in a JSON file with a remote reference to another JSON
        file
    WHEN init_yaml is called with the file
    THEN a valid model factory is returned.
    """
    # Defining specification
    base_spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {"column": {"$ref": "remote_spec.yaml#/Column"}},
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    remote_spec = {"Column": {"type": "integer", "x-primary-key": True}}

    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(base_spec))
    remote_spec_file = directory / "remote_spec.yaml"
    remote_spec_file.write_text(yaml.dump(remote_spec))

    # Creating model factory
    base, model_factory = open_alchemy.init_yaml(str(spec_file), define_all=False)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    value = 0
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value


@pytest.mark.integration
def test_init_yaml_import_error():
    """
    GIVEN yaml package is not available
    WHEN init_yaml is called
    THEN ImportError is raised.
    """
    with mock.patch.dict("sys.modules", {"yaml": None}):
        with pytest.raises(ImportError):
            open_alchemy.init_yaml("some file")


@pytest.mark.integration
def test_import_base_initial():
    """
    GIVEN
    WHEN
    THEN ImportError is raised when Base is imported from open_alchemy.models.
    """
    # pylint: disable=import-error,import-outside-toplevel,unused-import
    with pytest.raises(ImportError):
        from open_alchemy.models import Base  # noqa: F401


@pytest.mark.integration
def test_import_base(tmp_path):
    """
    GIVEN specification file
    WHEN init_yaml is called with the specification file
    THEN Base can be imported from open_alchemy.models.
    """
    # pylint: disable=import-error,import-outside-toplevel,unused-import
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(BASIC_SPEC))

    # Creating model factory
    open_alchemy.init_yaml(str(spec_file))

    from open_alchemy.models import Base  # noqa: F401


@pytest.mark.integration
def test_import_model(engine, sessionmaker, tmp_path):
    """
    GIVEN specification stored in a YAML file
    WHEN init_yaml is called with the file
    THEN the model is importable from open_alchemy.models.
    """
    # pylint: disable=import-error,import-outside-toplevel
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(BASIC_SPEC))

    # Creating model factory
    open_alchemy.init_yaml(str(spec_file), define_all=True)

    # Creating models
    from open_alchemy.models import Base

    Base.metadata.create_all(engine)

    # Creating model instance
    from open_alchemy.models import Table

    value = 0
    model_instance = Table(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(Table).first()
    assert queried_model.column == value


@pytest.mark.integration
def test_import_many_to_many_association(engine, sessionmaker, tmp_path):
    """
    GIVEN many to many specification stored in a YAML file
    WHEN init_yaml is called with the file
    THEN the association is importable from open_alchemy.models.
    """
    # pylint: disable=import-error,import-outside-toplevel
    spec = {
        "components": {
            "schemas": {
                "RefTable": {
                    "properties": {
                        "column": {"type": "integer", "x-primary-key": True}
                    },
                    "x-tablename": "ref_table",
                    "type": "object",
                    "x-secondary": "association",
                },
                "Table": {
                    "properties": {
                        "column": {"type": "integer", "x-primary-key": True},
                        "ref_tables": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/RefTable"},
                        },
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(spec))

    # Creating model factory
    open_alchemy.init_yaml(str(spec_file), define_all=True)

    # Creating models
    from open_alchemy.models import Base

    Base.metadata.create_all(engine)

    # Creating model instance
    from open_alchemy.models import RefTable
    from open_alchemy.models import Table
    from open_alchemy.models import association

    ref_instance = RefTable(column=11)
    model_instance = Table(column=12, ref_tables=[ref_instance])
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_association = session.query(association).first()
    assert queried_association == (12, 11)


@pytest.mark.integration
def test_models_file(tmp_path):
    """
    GIVEN specification stored in a YAML file
    WHEN init_yaml is called with the file and a models file path
    THEN the models are written to the models file.
    """
    # pylint: disable=import-error,import-outside-toplevel
    # Generate spec file
    directory = tmp_path / "specs"
    directory.mkdir()
    spec_file = directory / "spec.yaml"
    spec_file.write_text(yaml.dump(BASIC_SPEC))

    # Create models file
    models_file = directory / "models.py"

    # Creating model factory
    open_alchemy.init_yaml(
        str(spec_file), define_all=True, models_filename=str(models_file)
    )

    # Check models file contents
    models_file_contents = models_file.read_text()
    docstring = '"""Autogenerated SQLAlchemy models based on OpenAlchemy models."""'
    additional_import = ""
    if sys.version_info[1] < 8:
        additional_import = """
import typing_extensions"""
    expected_td_base = "typing.TypedDict"
    if sys.version_info[1] < 8:
        expected_td_base = "typing_extensions.TypedDict"
    expected_model_base = "typing.Protocol"
    if sys.version_info[1] < 8:
        expected_model_base = "typing_extensions.Protocol"
    expected_contents = f'''{docstring}
# pylint: disable=no-member,super-init-not-called,unused-argument

import typing

import sqlalchemy{additional_import}
from sqlalchemy import orm

from open_alchemy import models

Base = models.Base  # type: ignore


class TableDict({expected_td_base}, total=False):
    """TypedDict for properties that are not required."""

    column: typing.Optional[int]


class TTable({expected_model_base}):
    """
    SQLAlchemy model protocol.

    Attrs:
        column: The column of the Table.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column: 'sqlalchemy.Column[typing.Optional[int]]'

    def __init__(self, column: typing.Optional[int] = None) -> None:
        """
        Construct.

        Args:
            column: The column of the Table.

        """
        ...

    @classmethod
    def from_dict(cls, column: typing.Optional[int] = None) -> "TTable":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            column: The column of the Table.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TTable":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> TableDict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Table: typing.Type[TTable] = models.Table  # type: ignore
'''
    assert models_file_contents == expected_contents


@pytest.mark.integration
def test_build_json(tmp_path):
    """
    GIVEN spec, package name and distribution path
    WHEN build_json is called with the path to the file with the spec, package name and
        distribution path
    THEN the setup.py, MANIFEST.in, spec.json and __init__.py files are created.
    """
    dist = tmp_path / "dist"
    dist.mkdir()

    name = "app_models"
    version = "version 1"
    spec = {
        "info": {
            "version": version,
        },
        "components": {
            "schemas": {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                }
            }
        },
    }

    spec_dir = tmp_path / name
    spec_dir.mkdir(parents=True, exist_ok=True)
    spec_path = spec_dir / "spec.json"
    with open(spec_path, "w") as out_file:
        out_file.write(json.dumps(spec))

    open_alchemy.build_json(str(spec_path), package_name=name, dist_path=str(dist))

    # Define generated project directories
    project_path = dist / name
    package_path = project_path / name

    # Check setup file
    expected_setup_path = project_path / "setup.py"
    assert expected_setup_path.is_file()
    with open(expected_setup_path) as in_file:
        setup_contents = in_file.read()

    assert name in setup_contents
    assert version in setup_contents

    # Check manifest file
    expected_manifest_path = project_path / "MANIFEST.in"
    assert expected_manifest_path.is_file()
    with open(expected_manifest_path) as in_file:
        manifest_contents = in_file.read()
    assert name in manifest_contents

    # Check spec file
    expected_spec_path = package_path / "spec.json"
    assert expected_spec_path.is_file()
    with open(expected_spec_path) as in_file:
        spec_contents = in_file.read()
    assert '"Schema"' in spec_contents
    assert '"id"' in spec_contents

    # Check init file
    expected_init_path = package_path / "__init__.py"
    assert expected_init_path.is_file()
    with open(expected_init_path) as in_file:
        init_contents = in_file.read()
    assert "class SchemaDict" in init_contents
    assert "id: typing.Optional[int]" in init_contents
    assert "class TSchema" in init_contents
    assert "id: 'sqlalchemy.Column[typing.Optional[int]]'" in init_contents
    assert "Schema: typing.Type[TSchema]" in init_contents


@pytest.mark.integration
def test_build_yaml(tmp_path):
    """
    GIVEN spec, package name and distribution path
    WHEN build_json is called with the path to the file with the spec, package name and
        distribution path
    THEN the setup.py, MANIFEST.in, spec.json and __init__.py files are created.
    """
    dist = tmp_path / "dist"
    dist.mkdir()

    name = "app_models"
    version = "version 1"
    spec = {
        "info": {
            "version": version,
        },
        "components": {
            "schemas": {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                }
            }
        },
    }

    spec_path = tmp_path / "spec.yaml"
    with open(spec_path, "w") as out_file:
        out_file.write(yaml.dump(spec))

    open_alchemy.build_yaml(str(spec_path), package_name=name, dist_path=str(dist))

    # Check setup file
    expected_setup_path = tmp_path / "dist" / name / "setup.py"
    assert expected_setup_path.is_file()
    with open(expected_setup_path) as in_file:
        setup_contents = in_file.read()

    assert name in setup_contents
    assert version in setup_contents

    # Check manifest file
    expected_manifest_path = tmp_path / "dist" / name / "MANIFEST.in"
    assert expected_manifest_path.is_file()
    with open(expected_manifest_path) as in_file:
        manifest_contents = in_file.read()
    assert name in manifest_contents

    # Check spec file
    expected_spec_path = tmp_path / "dist" / name / name / "spec.json"
    assert expected_spec_path.is_file()
    with open(expected_spec_path) as in_file:
        spec_contents = in_file.read()
    assert '"Schema"' in spec_contents
    assert '"id"' in spec_contents

    # Check init file
    expected_init_path = tmp_path / "dist" / name / name / "__init__.py"
    assert expected_init_path.is_file()
    with open(expected_init_path) as in_file:
        init_contents = in_file.read()
    assert "class SchemaDict" in init_contents
    assert "id: typing.Optional[int]" in init_contents
    assert "class TSchema" in init_contents
    assert "id: 'sqlalchemy.Column[typing.Optional[int]]'" in init_contents
    assert "Schema: typing.Type[TSchema]" in init_contents


@pytest.mark.integration
def test_build_yaml_import_error():
    """
    GIVEN yaml package is not available
    WHEN build_yaml is called
    THEN ImportError is raised.
    """
    with mock.patch.dict("sys.modules", {"yaml": None}):
        with pytest.raises(ImportError):
            open_alchemy.build_yaml("some file", "some package", "some path")
