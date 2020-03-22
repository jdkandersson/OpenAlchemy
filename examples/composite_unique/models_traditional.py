import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    """Person that works for a company."""

    __tablename__ = "employee"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    address = sa.Column(sa.String)
    division = sa.Column(sa.String)


sa.UniqueConstraint(None, Employee.address, Employee.division)
