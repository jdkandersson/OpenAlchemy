"""Tests for the package builder."""

import pytest

from open_alchemy import build
from open_alchemy import exceptions


@pytest.mark.parametrize(
    "spec",
    [
        pytest.param(True, id="base invalid"),
        pytest.param({"components": {"schemas": {}}}, id="no schemas"),
        pytest.param(
            {
                "components": {
                    "schemas": {
                        "Schema1": {
                            "x-tablename": "schema_1",
                        }
                    }
                }
            },
            id="schema invalid",
        ),
    ],
)
@pytest.mark.build
def test_get_schemas_invalid(spec):
    """
    GIVEN invalid spec
    WHEN get_schemas is called
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(exceptions.MalformedSchemaError):
        build.get_schemas(spec=spec)


@pytest.mark.build
def test_get_schemas_valid():
    """
    GIVEN invalid spec
    WHEN get_schemas is called
    THEN MalformedSchemaError is raised.
    """
    spec = {
        "components": {
            "schemas": {
                "Schema1": {
                    "type": "object",
                    "x-tablename": "schema_1",
                    "properties": {"id": {"type": "integer"}},
                }
            }
        }
    }

    returned_schemas = build.get_schemas(spec=spec)

    assert returned_schemas == {
        "Schema1": {
            "type": "object",
            "x-tablename": "schema_1",
            "properties": {"id": {"type": "integer"}},
        }
    }


@pytest.mark.build
def test_generate_spec():
    """
    GIVEN schemas
    WHEN generate_spec is called with the schemas
    THEN the spec.json file contents with the schemas are returned.
    """
    schemas = {
        "Schema1": {
            "type": "object",
            "x-tablename": "schema_1",
            "properties": {"id": {"type": "integer"}},
        }
    }

    returned_contents = build.generate_spec(schemas=schemas)

    expected_contents = (
        '{"components":{"schemas":{"Schema1":'
        '{"type":"object","x-tablename":"schema_1",'
        '"properties":{"id":{"type":"integer"}}}}}}'
    )

    assert returned_contents == expected_contents


@pytest.mark.build
def test_generate_setup():
    """
    GIVEN name and version
    WHEN generate_setup is called with the name and version
    THEN the setup.py file contents with the name and version are returned.
    """
    name = "name 1"
    version = "version 1"

    returned_contents = build.generate_setup(name=name, version=version)

    expected_contents = """import setuptools

setuptools.setup(
    name="name 1",
    version="version 1",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "OpenAlchemy",
    ],
    include_package_data=True,
)
"""

    assert returned_contents == expected_contents


@pytest.mark.build
def test_generate_init_open_alchemy():
    """
    GIVEN name and version
    WHEN generate_init_open_alchemy is called with the name and version
    THEN the setup.py file contents with the name and version are returned.
    """
    returned_contents = build.generate_init_open_alchemy()

    expected_contents = """import pathlib

from open_alchemy import init_json

parent_path = pathlib.Path(__file__).parent.absolute()
init_json(parent_path / "spec.json")"""

    assert returned_contents == expected_contents
