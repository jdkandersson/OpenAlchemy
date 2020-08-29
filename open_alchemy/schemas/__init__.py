"""Performs operations on the schemas to prepare them for further processing."""

from .. import types as _types
from . import artifacts
from . import backref
from . import foreign_key
from . import helpers
from . import validation


def process(*, schemas: _types.Schemas) -> None:
    """
    Pre-process schemas.

    The processing actions executed are:
    1. Calculate the back references.

    Args:
        schemas: The schemas to pre-process in place.

    """
    validation.process(schemas=schemas)
    backref.process(schemas=schemas)
    foreign_key.process(schemas=schemas)
