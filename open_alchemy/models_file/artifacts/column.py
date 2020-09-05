"""Calculate the column artifacts for a model."""

import itertools
import typing

from open_alchemy import schemas

from .. import types
from . import type_


def calculate(
    *, artifacts: schemas.artifacts.types.ModelArtifacts
) -> typing.List[types.ColumnArtifacts]:
    """
    Calculate the column artifacts from model schema artifacts.

    Args:
        artifacts: The schema artifacts for a model.

    Returns:
        The artifacts for the columns.

    """
    # Process properties
    no_backref_properties = filter(
        lambda args: args[1].type != schemas.helpers.property_.type_.Type.BACKREF,
        artifacts.properties,
    )
    no_backref_no_dict_ignore_properties = filter(
        lambda args: not (
            args[1].type == schemas.helpers.property_.type_.Type.SIMPLE
            and args[1].extension.dict_ignore
        ),
        no_backref_properties,
    )
    properties_columns = map(
        lambda args: types.ColumnArtifacts(
            name=args[0],
            type=type_.model(artifacts=args[1]),
            description=args[1].description,
        ),
        no_backref_no_dict_ignore_properties,
    )

    # Process back references
    backrefs_columns = map(
        lambda args: types.ColumnArtifacts(
            name=args[0],
            type=f'typing.Optional["T{args[1].child}"]'
            if args[1].type == schemas.artifacts.types.BackrefSubType.OBJECT
            else f'typing.Sequence["T{args[1].child}"]',
            description=None,
        ),
        artifacts.backrefs,
    )

    return list(itertools.chain(properties_columns, backrefs_columns))
