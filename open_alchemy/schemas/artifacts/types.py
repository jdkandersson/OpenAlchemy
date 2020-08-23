"""The artifact types."""

import typing


class ModelArtifacts(typing.NamedTuple):
    """Information about a model."""

    tablename: str
    inherits: typing.Optional[bool]
