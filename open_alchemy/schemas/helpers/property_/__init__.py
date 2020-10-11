"""Helpers for properties."""

from . import relationship
from . import simple
from . import type_

TYPES = {"object", "array"}.union(simple.TYPES)
