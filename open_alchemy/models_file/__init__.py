"""Generate the models file."""

from open_alchemy import schemas
from open_alchemy.facades import code_formatter

from . import model as _model
from . import models as _models


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
            artifacts.items(),
        )
    )
    raw_source = _models.generate(models=model_sources)
    return code_formatter.apply(source=raw_source)
