"""Types for model generation."""

import dataclasses
import typing


@dataclasses.dataclass
class ColumnArtifacts:
    """Artifacts for the column portion of a model template."""

    name: str
    type: str


@dataclasses.dataclass
class ModelArtifacts:
    """Artifacts for a model template."""

    name: str
    columns: typing.List[ColumnArtifacts]
