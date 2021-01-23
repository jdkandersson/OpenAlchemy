"""Generate the models file."""

from open_alchemy.facades import code_formatter
from open_alchemy.schemas.artifacts.types import ModelsModelArtifacts

from . import model as _model
from . import models as _models


def generate(*, artifacts: ModelsModelArtifacts) -> str:
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
