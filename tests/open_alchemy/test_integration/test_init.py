"""Integration tests for initialization."""

import json
import sys
from unittest import mock

import pytest
import sqlalchemy
import yaml

import open_alchemy


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
        base=base, spec=spec, define_all=True, models_filename=None
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
        base=mock.MagicMock, spec={"components": {"schemas": {}}}
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
        base=mock.MagicMock, spec={"components": {"schemas": {}}}
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
    assert isinstance(model.column.type, sqlalchemy.Integer)


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
    expected_base = "typing.TypedDict"
    if sys.version_info[1] < 8:
        expected_base = "typing_extensions.TypedDict"
    expected_contents = f'''{docstring}
# pylint: disable=no-member,useless-super-delegation

import typing

import sqlalchemy{additional_import}
from sqlalchemy import orm

from open_alchemy import models


class TableDict({expected_base}, total=False):
    """TypedDict for properties that are not required."""

    column: typing.Optional[int]


class Table(models.Table):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column: typing.Optional[int]

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Table":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> TableDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()
'''
    assert models_file_contents == expected_contents
