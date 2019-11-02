"""Functions handling API endpoints."""

from database import db
from openapi_sqlalchemy.models import Employee


def _employee_to_dict(employee):
    """Transform Employee to dictionary."""
    return {
        "id": employee.id,
        "name": employee.name,
        "division": employee.division,
        "salary": employee.salary,
    }


def search():
    """Get all employees from the database."""
    employees = db.session.query(Employee).all()
    employee_dicts = map(lambda employee: _employee_to_dict(employee), employees)
    return list(employee_dicts)


def post(body):
    """Save an employee to the database."""
    if db.session.query(Employee).filter_by(id=body["id"]).first() is not None:
        return ("Employee already exists.", 400)
    employee = Employee(**body)
    db.session.add(employee)
    db.session.commit()


def get(id):
    """Get an employee from the database."""
    employee = db.session.query(Employee).filter_by(id=id).first()
    if employee is None:
        return ("Employee not found.", 404)
    return _employee_to_dict(employee)


def patch(body, id):
    """Update an employee in the dayabase."""
    employee = db.session.query(Employee).filter_by(id=id).first()
    if employee is None:
        return ("Employee not found.", 404)
    employee.name = body["name"]
    employee.division = body["division"]
    employee.salary = body["salary"]
    db.session.commit()
    return 200


def delete(id):
    """Delete an employee from the database."""
    result = db.session.query(Employee).filter_by(id=id).delete()
    if not result:
        return ("Employee not found.", 404)
    db.session.commit()
    return 200
