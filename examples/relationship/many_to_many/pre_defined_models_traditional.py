import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Project(Base):
    """A large sized business objective."""

    __tablename__ = "project"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


class Employee(Base):
    """Person that works for a company."""

    __tablename__ = "employee"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    projects = sa.orm.relationship("Project", secondary="project_employee")


class EmployeeProject(Base):
    """Person that works for a company."""

    __tablename__ = "project_employee"
    employee_id = sa.Column(sa.Integer, sa.ForeignKey("employee.id"), primary_key=True)
    employee_id = sa.Column(sa.Integer, sa.ForeignKey("project.id"), primary_key=True)
