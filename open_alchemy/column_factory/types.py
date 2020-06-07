"""Types for column factory."""

import typing

from open_alchemy import facades

TReturnValue = typing.List[
    typing.Tuple[
        str,
        typing.Union[facades.sqlalchemy.column.Column, facades.sqlalchemy.Relationship],
    ]
]
