"""Tests for the package builder."""

import pytest

from open_alchemy import build


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
