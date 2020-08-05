"""Helpers to process schemas."""

import itertools
import typing

from ... import types
from . import iterate


class Artifacts(typing.NamedTuple):
    """The return value of _calculate_schema."""

    schema_name: str
    property_name: str
    property_schema: types.Schema


ArtifactsIter = typing.Iterator[Artifacts]
ArtifactsGroupedIter = typing.Iterator[typing.Tuple[str, ArtifactsIter]]
SchemaIter = typing.Iterable[typing.Tuple[str, types.Schema]]
TGetSchemaArtifacts = typing.Callable[[types.Schemas, str, types.Schema], ArtifactsIter]


def get_artifacts(
    *, schemas: types.Schemas, get_schema_artifacts: TGetSchemaArtifacts
) -> ArtifactsIter:
    """
    Get all back reference information from the schemas.

    Takes all schemas, retrieves all constructable schemas, for each schema retrieves
    all back references and returns an iterable with all the captured back references.

    Args:
        schemas: The schemas to process.

    Returns:
        All backreference information.

    """
    # Retrieve all constructable schemas
    constructables = iterate.constructable(schemas=schemas)
    # Retrieve all artifacts
    artifacts_iters = map(
        lambda args: get_schema_artifacts(schemas, *args), constructables
    )
    # Unpack nested iterators
    return itertools.chain(*artifacts_iters)


TOutput = typing.TypeVar("TOutput")
TOutputIter = typing.Iterator[typing.Tuple[str, TOutput]]
TCalculateOutput = typing.Callable[[ArtifactsIter], TOutput]


def calculate_outputs(
    *, artifacts: ArtifactsIter, calculate_output: TCalculateOutput
) -> TOutputIter:
    """
    Convert artifacts iterator to an output iterator.

    Algorithm:
    1. sort and group by schema name and
    2. call calculate_output on the grouped artifacts.

    Args:
        artifacts: The artifacts to convert.
        calculate_output: Calculate the output from artifacts for a schema.

    Returns:
        An iterator with the converted output.

    """
    # Sort and group
    sorted_artifacts = sorted(artifacts, key=lambda backref: backref.schema_name)
    grouped_artifacts = itertools.groupby(
        sorted_artifacts, lambda backref: backref.schema_name
    )
    # Map to output
    return map(lambda args: (args[0], calculate_output(args[1])), grouped_artifacts)