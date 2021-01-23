"""Performs operations on the schemas to prepare them for further processing."""

import typing

from .. import types as _types
from . import association
from . import backref
from . import foreign_key
from . import validation


def process(
    *, schemas: _types.Schemas, spec_filename: typing.Optional[str] = None
) -> None:
    """
    Pre-process schemas.

    The processing actions executed are:
    1. Calculate the back references.

    Args:
        schemas: The schemas to pre-process in place.

    """
    validation.process(schemas=schemas, spec_filename=spec_filename)
    backref.process(schemas=schemas)
    foreign_key.process(schemas=schemas)
    association.process(schemas=schemas)
