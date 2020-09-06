"""Artifacts for the arguments."""

import itertools
import json
import typing

from open_alchemy import helpers
from open_alchemy import schemas
from open_alchemy import types as oa_types

from .. import types
from . import type_


class ReturnValue(typing.NamedTuple):
    """The return value for the calculated artifacts."""

    required: typing.List[types.ColumnArgArtifacts]
    not_required: typing.List[types.ColumnArgArtifacts]


def _get_read_only(
    artifacts: schemas.artifacts.types.TAnyPropertyArtifacts,
) -> typing.Optional[bool]:
    """Get read only for any property artifacts."""
    if artifacts.type == schemas.helpers.property_.type_.Type.SIMPLE:
        return artifacts.open_api.read_only
    if artifacts.type == schemas.helpers.property_.type_.Type.JSON:
        return artifacts.open_api.read_only
    return None


def _map_default(
    *, artifacts: schemas.artifacts.types.TAnyPropertyArtifacts
) -> oa_types.TColumnDefault:
    """
    Map default value from OpenAPI to be ready to be inserted into a Python file.

    First applies JSON formatting for a string and then using the type mapping helper
    function.

    Args:
        artifacts: The artifacts from which to map the default value.

    Returns:
        The mapped default value.

    """
    if artifacts.type != schemas.helpers.property_.type_.Type.SIMPLE:
        return None

    default = artifacts.open_api.default
    if default is None:
        return None

    # Escape string
    if artifacts.open_api.type == "string" and artifacts.open_api.format not in {
        "date",
        "date-time",
    }:
        default = json.dumps(default)

    # Handle bytes
    if artifacts.open_api.type == "string" and artifacts.open_api.format == "binary":
        return f"b{default}"

    # Map type
    mapped_default = helpers.oa_to_py_type.convert(
        value=default, type_=artifacts.open_api.type, format_=artifacts.open_api.format
    )

    # Get the repr if it isn't a float, bool, number nor str
    if isinstance(mapped_default, (int, float, str, bool)):
        return mapped_default
    return repr(mapped_default)


def _calculate(
    *,
    artifacts: typing.Iterable[
        typing.Tuple[str, schemas.artifacts.types.TAnyPropertyArtifacts]
    ],
) -> typing.Iterable[types.ColumnArgArtifacts]:
    """Calculate the arg artifacts from property artifacts."""
    no_backref_properties = filter(
        lambda args: args[1].type != schemas.helpers.property_.type_.Type.BACKREF,
        artifacts,
    )
    no_backref_no_dict_ignore_properties = filter(
        lambda args: not (
            args[1].type == schemas.helpers.property_.type_.Type.SIMPLE
            and args[1].extension.dict_ignore
        ),
        no_backref_properties,
    )
    return map(
        lambda args: types.ColumnArgArtifacts(
            name=args[0],
            init_type=type_.arg_init(artifacts=args[1]),
            from_dict_type=type_.arg_from_dict(artifacts=args[1]),
            default=_map_default(artifacts=args[1]),
            read_only=_get_read_only(artifacts=args[1]),
        ),
        no_backref_no_dict_ignore_properties,
    )


def calculate(*, artifacts: schemas.artifacts.types.ModelArtifacts) -> ReturnValue:
    """
    Calculate the args artifacts from model schema artifacts.

    Args:
        artifacts: The schema artifacts for a model.

    Returns:
        The artifacts for the args.

    """
    required = filter(lambda args: args[1].required, artifacts.properties)
    not_required = filter(lambda args: not args[1].required, artifacts.properties)

    # Process back references
    backrefs_columns = map(
        lambda args: types.ColumnArgArtifacts(
            name=args[0],
            init_type=f'typing.Optional["T{args[1].child}"]'
            if args[1].type == schemas.artifacts.types.BackrefSubType.OBJECT
            else f'typing.Optional[typing.Sequence["T{args[1].child}"]]',
            from_dict_type="",
            read_only=True,
        ),
        artifacts.backrefs,
    )

    return ReturnValue(
        required=list(_calculate(artifacts=required)),
        not_required=list(
            itertools.chain(_calculate(artifacts=not_required), backrefs_columns)
        ),
    )
