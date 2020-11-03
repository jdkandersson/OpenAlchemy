"""Execute external commands."""

import subprocess  # nosec: we are aware of the implications.
import typing

from .. import exceptions


def run(cmd: typing.List[str], cwd: str) -> typing.Tuple[str, str]:
    """
    Run a shell command.

    Args:
        cmd: The command to execute.
        cwd: The path where the command must be executed from.

    Returns:
        A tuple containing (stdout, stderr).

    """
    output = None
    try:
        # "nosec" is used here as we believe we followed the guidelines to use
        # subprocess securely:
        # https://security.openstack.org/guidelines/dg_use-subprocess-securely.html
        output = subprocess.run(  # nosec
            cmd,
            cwd=cwd,
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        raise exceptions.BuildError(str(exc)) from exc

    return output.stdout.decode("utf-8"), output.stderr.decode("utf-8")
