"""The artifact types."""

import dataclasses
import typing


@dataclasses.dataclass
class ModelArtifacts:
    """Information about a model."""

    tablename: str
    inherits: typing.Optional[bool]
    parent: typing.Optional[str]

    description: typing.Optional[str]

    mixins: typing.Optional[typing.List[str]]
