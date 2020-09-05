"""Generate the models file."""
# pylint: disable=useless-import-alias

import dataclasses
import typing

from open_alchemy import facades
from open_alchemy import schemas
from open_alchemy import types as oa_types

from . import artifacts as _artifacts
from . import model as _model
from . import models as _models
from . import types as types


def generate(*, artifacts: schemas.artifacts.types.ModelsModelArtifacts) -> str:
    """
    Generate the models file from schema artifacts.

    Args:
        artifacts: The artifacts from the schemas.

    Returns:
        The models file.

    """
    model_sources = list(
        map(
            lambda args: _model.generate(artifacts=args[1], name=args[0]),
            artifacts,
        )
    )
    raw_source = _models.generate(models=model_sources)
    return facades.code_formatter.apply(source=raw_source)
