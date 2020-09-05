"""Generate a model class based on artifacts."""

import typing

from open_alchemy import schemas
from open_alchemy import types as oa_types

from .. import artifacts as models_file_artifacts
from . import source as _source


def generate(*, artifacts: schemas.artifacts.types.ModelArtifacts, name: str) -> str:
    """
    Generate the class source from the schema.

    Args:
        schema: The schema of the model.
        name: The name of the model.

    Returns:
        The source code for the model class.

    """
    model_artifacts = models_file_artifacts.calculate(artifacts=artifacts, name=name)
    return _source.generate(artifacts=model_artifacts)
