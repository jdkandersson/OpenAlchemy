"""Tests for the command helper."""

import pytest

from open_alchemy import exceptions
from open_alchemy.helpers import command


@pytest.mark.helper
def test_run_error():
    """
    GIVEN a command that exits with a non-zero status
    WHEN run is called with the command
    THEN BuildError is raised.
    """
    with pytest.raises(exceptions.BuildError):
        command.run(["python", "-c", "import sys; sys.exit(1)"], ".")


@pytest.mark.helper
def test_run_success():
    """
    GIVEN a command that exits successfully
    WHEN run is called with the command
    THEN the stdout and stderr are returned.
    """
    stdout, stderr = command.run(
        ["python", "-c", "print('hello')"],
        ".",
    )

    assert "hello" in stdout
    assert stderr == ""
