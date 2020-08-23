import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import TimestampsMixin

Base = declarative_base()


class Employee(Base, TimestampsMixin):
    """Person that works for a company."""

    __tablename__ = "employee"
    __abstract__ = False

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, index=True)
    division = sa.Column(sa.String, index=True)
    salary = sa.Column(sa.Float)
