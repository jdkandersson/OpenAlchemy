import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


employee_project = sa.Table(
    "employee_project",
    Base.metadata,
    sa.Column("project_id", sa.Integer, sa.ForeignKey("project.id")),
    sa.Column("employee_id", sa.Integer, sa.ForeignKey("employee.id")),
)


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
