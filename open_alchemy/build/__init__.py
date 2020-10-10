"""Build a package with the OpenAlchemy models."""

import enum
import hashlib
import json
import pathlib
import subprocess  # nosec: we are aware of the implications.
import sys
import typing

import jinja2

from .. import exceptions
from .. import models_file as models_file_module
from .. import schemas as schemas_module
from .. import types

# TODO(rgreinho)): Fix above nosec it in the future when  # pylint: disable=W0511
# following issue is resolved:
# https://github.com/PyCQA/bandit/issues/211


_DIRECTORY = pathlib.Path(__file__).parent.absolute()
with open(_DIRECTORY / "setup.j2") as in_file:
    _SETUP_TEMPLATE = in_file.read()
with open(_DIRECTORY / "MANIFEST.j2") as in_file:
    _MANIFEST_TEMPLATE = in_file.read()
with open(_DIRECTORY / "init_init_open_alchemy.j2") as in_file:
    _INIT_INIT_OPEN_ALCHEMY_TEMPLATE = in_file.read()
with open(_DIRECTORY / "init.j2") as in_file:
    _INIT_TEMPLATE = in_file.read()


class PackageFormat(enum.Flag):
    """Define the available package formats for the build."""

    NONE = enum.auto()
    SDIST = enum.auto()
    WHEEL = enum.auto()


def validate_dist_format(format_) -> None:
    """
    Ensure a valid package format is provided.

    Raises a ``BuildError` exception if the format is invalid.

    Args:
        format_: the package format to validate
    """
    if format_ is not PackageFormat.NONE and PackageFormat.NONE in format_:
        raise exceptions.BuildError(
            "Combining `PackageFormat.NONE` with another package type "
            "prevents OpenAlchemy to determine if an archive should be "
            f"created or not: '{format_}'. Either specify 'PackageFormat.NONE' "
            "or the format(s) to build. "
        )


def get_schemas(*, spec: typing.Any) -> types.Schemas:
    """
    Get the schemas from the specification.

    Raises MalformedSchemaError if keys to the schemas are missing or the
    schemas are not valid.

    Args:
        spec: The spec to retrieve schemas from.

    Returns:
        The schemas after validation.

    """
    # Check to schemas
    result = schemas_module.validation.spec_validation.check(spec=spec)
    if not result.valid:
        raise exceptions.MalformedSchemaError(result.reason)

    # Check that there is at least 1 model
    assert isinstance(spec, dict)
    components = spec.get("components")
    assert isinstance(components, dict)
    schemas = components.get("schemas")
    assert isinstance(schemas, dict)
    one_model_result = schemas_module.validation.check_one_model(schemas=schemas)
    if not one_model_result.valid:
        raise exceptions.MalformedSchemaError(one_model_result.reason)

    # Check schemas
    schemas_module.process(schemas=schemas)

    return schemas


def generate_spec(*, schemas: types.Schemas) -> str:
    """
    Generate the spec.json file contents.

    Args:
        schemas: The schemas to generate the spec for.

    Returns:
        The JSON encoded schemas.

    """
    return json.dumps({"components": {"schemas": schemas}}, separators=(",", ":"))


def calculate_version(*, spec: typing.Any, spec_str: str) -> str:
    """
    Calculate the version for a spec.

    The algorithm is:
    1. look for the API version in the spec and return or
    2. return the hash of the spec.

    Args:
        spec: The spec as a dictionary.
        spec_str: The spec after it has been converted to string.

    Returns:
        The version of the spec.

    """
    try:
        spec_version = spec["info"]["version"]
        if isinstance(spec_version, str):
            return spec_version
    except (KeyError, TypeError):
        pass

    return hashlib.sha1(spec_str.encode()).hexdigest()[:20]


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


def generate_manifest(*, name: str) -> str:
    """
    Generate the content of the MANIFEST.in file.

    Args:
        name: The name of the package.

    Returns:
        The contents of the MANIFEST.in file for the models package.

    """
    template = jinja2.Template(_MANIFEST_TEMPLATE)

    return template.render(
        name=name,
    )


def generate_init_open_alchemy() -> str:
    """
    Generate the OpenAlchemy initialization component of the __init__ file.

    Returns:
        The OpenAlchemy initialization portion of the __init__ file.

    """
    template = jinja2.Template(_INIT_INIT_OPEN_ALCHEMY_TEMPLATE)

    return template.render()


def generate_init_models_file(schemas: types.Schemas) -> str:
    """
    Generate the models file component of init.

    Args:
        schemas: All defined schemas.

    Returns:
        The models file component of the schemas.

    """
    schemas_module.backref.process(schemas=schemas)
    artifacts = schemas_module.artifacts.get_from_schemas(
        schemas=schemas, stay_within_model=False
    )
    return models_file_module.generate(artifacts=artifacts)


def generate_init(open_alchemy: str, models_file: str) -> str:
    """
    Generate the contents for the __init__.py file.

    Args:
        open_alchemy: The OpenAlchemy portion of the __init__ file.
        models_file: The models file portion of the __init__ file.

    Returns:
        The contents of the __init__ file.

    """
    template = jinja2.Template(_INIT_TEMPLATE)

    return template.render(
        open_alchemy=open_alchemy,
        models_file=models_file,
    )


def dump(
    *, path: str, name: str, setup: str, manifest: str, spec: str, init: str
) -> None:
    """
    Dump the files needed for the package at a path.

    Args:
        path: The path that will be the root of the package.
        name: The name of the package.
        setup: The contents for the setup file.
        manifest: The contents for the manifest file.
        spec: The contents for the spec file.
        init: The contents for the __init__ file.

    """
    try:
        # Write files at the root of the project directory.
        directory = pathlib.Path(path) / name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "setup.py").write_text(setup)
        (directory / "MANIFEST.in").write_text(manifest)

        # Write files in the package directory.
        package = directory / name
        package.mkdir(parents=True, exist_ok=True)
        (package / "spec.json").write_text(spec)
        (package / "__init__.py").write_text(init)
    except OSError as exc:
        raise exceptions.BuildError(str(exc)) from exc


def build_dist(name: str, path: str, format_: PackageFormat) -> None:
    """
    Build a distribution package.

    The formats can be combined with the bitwise operator "or" (``|``), for
    instance, building both sdist and wheel packages can be specified like this:

    .. code-block:: python

        format_=PackageFormat.SDIST|PackageFormat.WHEEL

    Args:
        path: The package directory.
        format: The package format to build.
    """
    if PackageFormat.SDIST in format_:
        build_sdist(name, path)
    if PackageFormat.WHEEL in format_:
        build_wheel(name, path)


def build_sdist(name: str, path: str) -> None:
    """
    Build a .tar.gz source distribution and place it in a "dist" folder.

    The "dist" folder is located at the root of the project.

    Args:
        path: The package directory.
    """
    pkg_dir = pathlib.Path(path) / name
    run([sys.executable, "setup.py", "sdist"], str(pkg_dir))


def build_wheel(name: str, path: str) -> None:
    """
    Build a .whl package and place it in a "dist" folder.

    The "dist" folder is located at the root of the project.

    Args:
        path: The package directory.
    """
    pkg_dir = pathlib.Path(path) / name
    try:
        run([sys.executable, "setup.py", "bdist_wheel"], str(pkg_dir))
    except exceptions.BuildError as exc:
        raise RuntimeError(
            "Building a wheel package requires the wheel package. "
            "Try `pip install wheel`."
        ) from exc


def run(cmd: typing.List[str], cwd: str) -> typing.Tuple[str, str]:
    """
    Run a shell command.

    Args:
        cmd: The command to execute.
        cwd: The path where the command must be executed from.

    Returns:
        A tuple containing (stdout, stderr).

    """
    output = None
    try:
        # "nosec" is used here as we believe we followed the guidelines to use
        # subprocess securely:
        # https://security.openstack.org/guidelines/dg_use-subprocess-securely.html
        output = subprocess.run(  # nosec
            cmd,
            cwd=cwd,
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        raise exceptions.BuildError(str(exc)) from exc

    return output.stdout.decode("utf-8"), output.stderr.decode("utf-8")


def execute(
    *,
    spec: typing.Any,
    name: str,
    path: str,
    format_: PackageFormat,
) -> None:
    """
    Execute the build for a spec.

    Args:
        spec: The spec to execute the build on.
        name: The name of the package.
        path: The build output path.
        format_: The format of the distribution package to build.

    """
    validate_dist_format(format_)
    schemas = get_schemas(spec=spec)
    spec_str = generate_spec(schemas=schemas)
    version = calculate_version(spec=spec, spec_str=spec_str)
    setup = generate_setup(name=name, version=version)
    manifest = generate_manifest(name=name)

    init_open_alchemy = generate_init_open_alchemy()
    init_models_file = generate_init_models_file(schemas=schemas)
    init = generate_init(open_alchemy=init_open_alchemy, models_file=init_models_file)

    dump(
        path=path,
        name=name,
        setup=setup,
        manifest=manifest,
        spec=spec_str,
        init=init,
    )

    # Build a distributable archive if needed.
    build_dist(name, path, format_)
