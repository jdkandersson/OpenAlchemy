"""SQLAlchemy models based on models constructed by OpenAlchemy."""
# pylint: disable=no-member

import typing

from open_alchemy import models


class Employee(models.Employee):
    """Employee SQLAlchemy model."""

    id: int
    name: str
    division: str
    salary: typing.Optional[float]
