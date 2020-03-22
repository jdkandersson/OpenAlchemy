import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PayInfo(Base):
    """Information on how to pay an employee."""

    __tablename__ = "pay_info"
    id = sa.Column(sa.Integer, primary_key=True)
    account_number = sa.Column(sa.String)


class Employee(Base):
    """Person that works for a company."""

    __tablename__ = "employee"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    pay_info_id = sa.Column(sa.Integer, sa.ForeignKey("pay_info.id"))
    pay_info = sa.orm.relationship("PayInfo", uselist=False)
