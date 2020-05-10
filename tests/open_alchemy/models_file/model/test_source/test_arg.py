"""Tests for model."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file

_ArgArtifacts = models_file.types.ArgArtifacts
_ColumnArgArtifacts = models_file.types.ColumnArgArtifacts


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (_ArgArtifacts(required=[], not_required=[]), ""),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[],
            ),
            ", column_1: init_type_1",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
            ),
            ", column_1: init_type_1 = None",
        ),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    ),
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    ),
                ],
                not_required=[],
            ),
            ", column_1: init_type_1, column_2: init_type_2",
        ),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    )
                ],
            ),
            ", column_1: init_type_1, column_2: init_type_2 = None",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    ),
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    ),
                ],
            ),
            ", column_1: init_type_1 = None, column_2: init_type_2 = None",
        ),
    ],
    ids=[
        "empty",
        "single required",
        "single not required",
        "multiple required",
        "multiple required and not required",
        "multiple not required",
    ],
)
@pytest.mark.models_file
def test_arg_init(artifacts, expected_source):
    """
    GIVEN artifacts
    WHEN arg_init is called with the artifacts
    THEN the expected source is returned.
    """
    source = models_file._model._source.arg_init(artifacts=artifacts)

    assert source == expected_source


TEST_REMOVE_READ_ONLY_ARGS_DATA = [
    pytest.param(
        _ArgArtifacts(required=[], not_required=[]),
        _ArgArtifacts(required=[], not_required=[]),
        id="empty",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1", init_type="init_type_1", from_dict_type="fd_type_1"
                )
            ],
            not_required=[],
        ),
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1", init_type="init_type_1", from_dict_type="fd_type_1"
                )
            ],
            not_required=[],
        ),
        id="single required not read only",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="init_type_1",
                    from_dict_type="fd_type_1",
                    read_only=False,
                )
            ],
            not_required=[],
        ),
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="init_type_1",
                    from_dict_type="fd_type_1",
                    read_only=False,
                )
            ],
            not_required=[],
        ),
        id="single required read only False",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="init_type_1",
                    from_dict_type="fd_type_1",
                    read_only=True,
                )
            ],
            not_required=[],
        ),
        _ArgArtifacts(required=[], not_required=[]),
        id="single required read only",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1", init_type="init_type_1", from_dict_type="fd_type_1"
                ),
                _ColumnArgArtifacts(
                    name="column_2", init_type="init_type_2", from_dict_type="fd_type_2"
                ),
            ],
            not_required=[],
        ),
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1", init_type="init_type_1", from_dict_type="fd_type_1"
                ),
                _ColumnArgArtifacts(
                    name="column_2", init_type="init_type_2", from_dict_type="fd_type_2"
                ),
            ],
            not_required=[],
        ),
        id="multiple required no read only",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="init_type_1",
                    from_dict_type="fd_type_1",
                    read_only=True,
                ),
                _ColumnArgArtifacts(
                    name="column_2", init_type="init_type_2", from_dict_type="fd_type_2"
                ),
            ],
            not_required=[],
        ),
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_2", init_type="init_type_2", from_dict_type="fd_type_2"
                )
            ],
            not_required=[],
        ),
        id="multiple required first read only",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1", init_type="init_type_1", from_dict_type="fd_type_1"
                ),
                _ColumnArgArtifacts(
                    name="column_2",
                    init_type="init_type_2",
                    from_dict_type="fd_type_2",
                    read_only=True,
                ),
            ],
            not_required=[],
        ),
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1", init_type="init_type_1", from_dict_type="fd_type_1"
                )
            ],
            not_required=[],
        ),
        id="multiple required second read only",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="init_type_1",
                    from_dict_type="fd_type_1",
                    read_only=True,
                ),
                _ColumnArgArtifacts(
                    name="column_2",
                    init_type="init_type_2",
                    from_dict_type="fd_type_2",
                    read_only=True,
                ),
            ],
            not_required=[],
        ),
        _ArgArtifacts(required=[], not_required=[]),
        id="multiple required all read only",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[],
            not_required=[
                _ColumnArgArtifacts(
                    name="column_1", init_type="init_type_1", from_dict_type="fd_type_1"
                )
            ],
        ),
        _ArgArtifacts(
            required=[],
            not_required=[
                _ColumnArgArtifacts(
                    name="column_1", init_type="init_type_1", from_dict_type="fd_type_1"
                )
            ],
        ),
        id="single not required not read only",
    ),
    pytest.param(
        _ArgArtifacts(
            required=[],
            not_required=[
                _ColumnArgArtifacts(
                    name="column_1",
                    init_type="init_type_1",
                    from_dict_type="fd_type_1",
                    read_only=True,
                )
            ],
        ),
        _ArgArtifacts(required=[], not_required=[]),
        id="single not required read only",
    ),
]


@pytest.mark.parametrize(
    "artifacts, expected_artifacts", TEST_REMOVE_READ_ONLY_ARGS_DATA
)
@pytest.mark.models_file
def test_remove_read_only_args(artifacts, expected_artifacts):
    """
    GIVEN input and expected artifacts
    WHEN remove_read_only_args is called
    THEN the expected artifacts are returned.
    """
    returned_artifacts = models_file._model._source.remove_read_only_args(
        artifacts=artifacts
    )

    assert returned_artifacts == expected_artifacts


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (_ArgArtifacts(required=[], not_required=[]), ""),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[],
            ),
            ", column_1: fd_type_1",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
            ),
            ", column_1: fd_type_1 = None",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                        default='"value 1"',
                    )
                ],
            ),
            ', column_1: fd_type_1 = "value 1"',
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                        read_only=True,
                    )
                ],
            ),
            "",
        ),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    ),
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    ),
                ],
                not_required=[],
            ),
            ", column_1: fd_type_1, column_2: fd_type_2",
        ),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    )
                ],
            ),
            ", column_1: fd_type_1, column_2: fd_type_2 = None",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    ),
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    ),
                ],
            ),
            ", column_1: fd_type_1 = None, column_2: fd_type_2 = None",
        ),
    ],
    ids=[
        "empty",
        "single required",
        "single not required",
        "single default",
        "single readOnly",
        "multiple required",
        "multiple required and not required",
        "multiple not required",
    ],
)
@pytest.mark.models_file
def test_arg_from_dict(artifacts, expected_source):
    """
    GIVEN artifacts
    WHEN arg_from_dict is called with the artifacts
    THEN the expected source is returned.
    """
    source = models_file._model._source.arg_from_dict(artifacts=artifacts)

    assert source == expected_source
