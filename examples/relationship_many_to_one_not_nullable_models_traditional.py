import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Division(Base):
    """Division of a company."""

    __tablename__ = "division"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


class Employee(Base):
    """Person that works for a company."""

    __tablename__ = "employee"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    division_id = sa.Column(sa.Integer, sa.ForeignKey("division.id"), nullable=False)
