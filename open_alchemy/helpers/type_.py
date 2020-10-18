"""Type information."""

SIMPLE_TYPES = {"integer", "number", "string", "boolean"}
TYPES = {"object", "array"}.union(SIMPLE_TYPES)
