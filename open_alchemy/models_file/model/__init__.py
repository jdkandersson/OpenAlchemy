"""Generate a model class based on artifacts."""

import typing

from open_alchemy import types as oa_types

from . import artifacts as _artifacts
from . import source as _source
from . import type_ as _type


def generate(*, schema: oa_types.Schema, name: str) -> str:
    """
    Generate the class source from the schema.

    Args:
        schema: The schema of the model.
        name: The name of the model.

    Returns:
        The source code for the model class.

    """
    artifacts = _artifacts.calculate(schema=schema, name=name)
    return _source.generate(artifacts=artifacts)
