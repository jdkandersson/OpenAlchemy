import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    """Person that works for a company."""

    __tablename__ = "employee"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, index=True, nullable=True)
    division = sa.Column(sa.String, index=True)
    salary = sa.Column(sa.Float)
