import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    """Person that works for a company."""

    __tablename__ = "employee"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    type = sa.Column(sa.String)

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "employee"}


class Manager(Employee):
    """Person that works for a company."""

    manager_data = sa.Column(sa.String)

    __mapper_args__ = {"polymorphic_identity": "manager"}


class Engineer(Employee):
    """Person that works for a company."""

    engineer_info = sa.Column(sa.String)

    __mapper_args__ = {"polymorphic_identity": "engineer"}
