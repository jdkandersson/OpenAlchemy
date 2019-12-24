"""Generate the models file."""
# pylint: disable=useless-import-alias

import typing

import black

from open_alchemy import types as oa_types

from . import model as _model
from . import models as _models
from . import types as types


class ModelsFile:
    """Keeps track of models and writes them as output."""

    def __init__(self):
        """Construct."""
        self._models: typing.List[str] = []

    def add_model(self, schema: oa_types.Schema, name: str) -> None:
        """
        Add model to be tracked.

        Args:
            schema: The schema of the model.
            name: The name of the model.

        """
        model_source = _model.generate(schema=schema, name=name)
        self._models.append(model_source)

    def generate_models(self) -> str:
        """
        Generate the models file.

        Returns:
            The source code for the models file.

        """
        raw_source = _models.generate(models=self._models)
        try:
            formatted_source = black.format_file_contents(
                src_contents=raw_source, fast=False, mode=black.FileMode()
            )
        except black.NothingChanged:
            formatted_source = raw_source
        return formatted_source
