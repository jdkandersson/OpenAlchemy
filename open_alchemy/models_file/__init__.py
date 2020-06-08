"""Generate the models file."""
# pylint: disable=useless-import-alias

import dataclasses
import typing

from open_alchemy import facades
from open_alchemy import types as oa_types

from . import model as _model
from . import models as _models
from . import types as types


class ModelsFile:
    """Keeps track of models and writes them as output."""

    def __init__(self):
        """Construct."""
        self._models: typing.Dict[str, oa_types.Schema] = {}

    def add_model(self, schema: oa_types.Schema, name: str) -> None:
        """
        Add model to be tracked.

        Args:
            schema: The schema of the model.
            name: The name of the model.

        """
        if name in self._models:
            return
        self._models[name] = schema

    def generate_models(self) -> str:
        """
        Generate the models file.

        Returns:
            The source code for the models file.

        """
        # Generate source code for each model
        model_sources: typing.List[str] = []
        for name, schema in self._models.items():
            model_source = _model.generate(schema=schema, name=name)
            model_sources.append(model_source)

        # Generate source code for models file
        raw_source = _models.generate(models=model_sources)
        return facades.code_formatter.apply(source=raw_source)
