"""Define the CLI module."""
import argparse
import logging
import pathlib

from open_alchemy import PackageFormat
from open_alchemy import build_json
from open_alchemy import build_yaml
from open_alchemy import exceptions
from open_alchemy import init_json
from open_alchemy import init_yaml

# Configure the logger.
logging.basicConfig(format="%(message)s", level=logging.INFO)

# Define constants.
VALID_EXTENSIONS = [".json", ".yml", ".yaml"]


def main() -> None:
    """Define the CLI entrypoint."""
    args = build_application_parser()
    try:
        args.func(args)
    except exceptions.CLIError as exc:
        logging.error("Cannot perform the operation: %s.", exc)


def validate_specfile(specfile: pathlib.Path) -> None:
    """
    Ensure the specfile is valid.

    The specification file must:
        * exist
        * have a valid extension (.json, .yml, or .yaml)

    Args:
        specfile: Path object representing the specification file.
    """
    # Ensure the file exists.
    if not specfile.exists():
        raise exceptions.CLIError(f"the specfile '{specfile}' cannot be found")

    # Ensure the extension is valid.
    ext = specfile.suffix.lower()
    if ext not in VALID_EXTENSIONS:
        raise exceptions.CLIError(
            f"specification format not supported: '{specfile}' "
            f"(valid extensions are {', '.join(VALID_EXTENSIONS)}, "
            "case insensitive)"
        )


def build_application_parser() -> argparse.Namespace:
    """Build the main parser and subparsers."""
    # Define the top level parser.
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands", help="subcommand help")

    # Define the parser for the "build" subcommand.
    build_parser = subparsers.add_parser(
        "build",
        description="Build a package with the SQLAlchemy models.",
        help="build a package",
    )
    build_parser.add_argument(
        "specfile", type=str, help="specify the specification file"
    )
    build_parser.add_argument("name", type=str, help="specify the package name")
    build_parser.add_argument("output", type=str, help="specify the output directory")
    build_parser.add_argument(
        "-f",
        "--format",
        type=str.lower,
        choices=["sdist", "wheel"],
        help="limit the format to either sdist or wheel, defaults to both",
    )
    build_parser.set_defaults(func=build)

    # Define the parser for the "generate" subcommand.
    generate_parser = subparsers.add_parser(
        "generate",
        description="Generate the SQLAlchemy models.",
        help="regenerate models",
    )
    generate_parser.add_argument(
        "specfile", type=str, help="specify the specification file"
    )
    generate_parser.add_argument("output", type=str, help="specify the output file")
    generate_parser.set_defaults(func=generate)

    # Return the parsed arguments for a particular command.
    return parser.parse_args()


def build(args: argparse.Namespace) -> None:
    """
    Define the build subcommand.

    Args:
        args: CLI arguments from the parser.
    """
    # Check the specfile.
    specfile = pathlib.Path(args.specfile)
    validate_specfile(specfile)

    # Select the builder method.
    builders = dict(zip(VALID_EXTENSIONS, [build_json, build_yaml, build_yaml]))

    # Choose the distributable format.
    fmt = {
        None: PackageFormat.SDIST | PackageFormat.WHEEL,
        "sdist": PackageFormat.SDIST,
        "wheel": PackageFormat.WHEEL,
    }

    # Build the package.
    builder = builders.get(specfile.suffix.lower())
    builder(args.specfile, args.name, args.output, fmt.get(args.format))  # type: ignore


def generate(args):
    """
    Define the generate subcommand.

    Args:
        args: CLI arguments from the parser.
    """
    # Check the specfile.
    specfile = pathlib.Path(args.specfile)
    validate_specfile(specfile)

    # Select the generator method.
    generators = dict(zip(VALID_EXTENSIONS, [init_json, init_yaml, init_yaml]))

    # Regenerate the models.
    generator = generators.get(specfile.suffix.lower())
    generator(args.specfile, models_filename=args.output)
