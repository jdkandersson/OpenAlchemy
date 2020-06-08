"""Apply automatic code formatting to source code."""

import black


def apply(*, source: str) -> str:
    """
    Apply automatic code formatting to source code.

    Args:
        source: The source code.

    Returns:
        The formatted source code.

    """
    try:
        return black.format_file_contents(
            src_contents=source, fast=False, mode=black.FileMode()
        )
    except black.NothingChanged:
        return source
