"""Calculate the model from the schema artifacts."""

import sys
import typing

from open_alchemy import schemas

from .. import types
from . import args as _args
from . import column as _column
from . import type_ as _type
from . import typed_dict as _typed_dict


def calculate(
    *, artifacts: schemas.artifacts.types.ModelArtifacts, name: str
) -> types.ModelArtifacts:
    """
    Calculate the model artifacts from the schema.

    Args:
        schema: The schema of the model
        name: The name of the model.

    Returns:
        The artifacts for the model.

    """
    columns = list(_column.calculate(artifacts=artifacts))
    typed_dict_required_props, typed_dict_not_required_props = _typed_dict.calculate(
        artifacts=artifacts
    )
    required_args, not_required_args = _args.calculate(artifacts=artifacts)

    # Calculate model parent class
    parent_cls: str
    if sys.version_info[1] < 8:
        parent_cls = "typing_extensions.Protocol"
    else:  # version compatibility
        parent_cls = "typing.Protocol"

    # Calculate whether property lists are empty, their names and parent class
    typed_dict_required_empty = not typed_dict_required_props
    typed_dict_not_required_empty = not typed_dict_not_required_props
    typed_dict_required_name = None
    typed_dict_not_required_name: typing.Optional[str] = f"{name}Dict"
    typed_dict_required_parent_class = None
    typed_dict_not_required_parent_class: typing.Optional[str]
    if sys.version_info[1] < 8:
        typed_dict_not_required_parent_class = "typing_extensions.TypedDict"
    else:  # version compatibility
        typed_dict_not_required_parent_class = "typing.TypedDict"
    if not typed_dict_required_empty and not typed_dict_not_required_empty:
        typed_dict_required_parent_class = typed_dict_not_required_parent_class
        typed_dict_required_name = f"_{name}DictBase"
        typed_dict_not_required_parent_class = typed_dict_required_name
    if not typed_dict_required_empty and typed_dict_not_required_empty:
        typed_dict_required_name = typed_dict_not_required_name
        typed_dict_not_required_name = None
        typed_dict_required_parent_class = typed_dict_not_required_parent_class
        typed_dict_not_required_parent_class = None

    return types.ModelArtifacts(
        sqlalchemy=types.SQLAlchemyModelArtifacts(
            name=name,
            columns=columns,
            empty=not columns,
            arg=types.ArgArtifacts(
                required=required_args, not_required=not_required_args
            ),
            parent_cls=parent_cls,
            description=artifacts.description,
        ),
        typed_dict=types.TypedDictArtifacts(
            required=types.TypedDictClassArtifacts(
                props=typed_dict_required_props,
                empty=typed_dict_required_empty,
                name=typed_dict_required_name,
                parent_class=typed_dict_required_parent_class,
            ),
            not_required=types.TypedDictClassArtifacts(
                props=typed_dict_not_required_props,
                empty=typed_dict_not_required_empty,
                name=typed_dict_not_required_name,
                parent_class=typed_dict_not_required_parent_class,
            ),
        ),
    )
