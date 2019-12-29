"""Generate the models file."""
# pylint: disable=useless-import-alias

import dataclasses
import typing

import black

from open_alchemy import types as oa_types

from . import model as _model
from . import models as _models
from . import types as types


@dataclasses.dataclass
class _Model:
    """Records a model to be processed."""

    name: str
    schema: oa_types.Schema


class ModelsFile:
    """Keeps track of models and writes them as output."""

    def __init__(self):
        """Construct."""
        self._models: typing.List[_Model] = []

    def add_model(self, schema: oa_types.Schema, name: str) -> None:
        """
        Add model to be tracked.

        Args:
            schema: The schema of the model.
            name: The name of the model.

        """
        self._models.append(_Model(name=name, schema=schema))

    def generate_models(self) -> str:
        """
        Generate the models file.

        Returns:
            The source code for the models file.

        """
        # Generate source code for each model
        model_sources: typing.List[str] = []
        for model in self._models:
            model_source = _model.generate(schema=model.schema, name=model.name)
            model_sources.append(model_source)

        # Generate source code for models file
        raw_source = _models.generate(models=model_sources)
        try:
            return black.format_file_contents(
                src_contents=raw_source, fast=False, mode=black.FileMode()
            )
        except black.NothingChanged:
            return raw_source
