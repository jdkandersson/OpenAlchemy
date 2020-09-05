"""Build a package with the OpenAlchemy models."""

import pathlib

import jinja2

_DIRECTORY = pathlib.Path(__file__).parent.absolute()
with open(_DIRECTORY / "setup.j2") as in_file:
    _SETUP_TEMPLATE = in_file.read()
with open(_DIRECTORY / "init_init_open_alchemy.j2") as in_file:
    _INIT_INIT_OPEN_ALCHEMY_TEMPLATE = in_file.read()


def generate_setup(*, name: str, version: str) -> str:
    """
    Generate the content of the setup.py file.

    Args:
        name: The name of the package.
        version: The version of the package.

    Returns:
        The contents of the setup.py file for the models package.

    """
    template = jinja2.Template(_SETUP_TEMPLATE)

    return template.render(
        name=name,
        version=version,
    )


def generate_init_open_alchemy() -> str:
    """
    Generate the OpenAlchemy initialization component of the __init__ file.

    Returns:
        The OpenAlchemy initialization portion of the __init__ file.

    """
    template = jinja2.Template(_INIT_INIT_OPEN_ALCHEMY_TEMPLATE)

    return template.render()
