"""Functions handling API endpoints."""

from models import Employee
from models import db


def search():
    """Get all employees from the database."""
    employees = Employee.query.all()
    employee_dicts = map(lambda employee: employee.to_dict(), employees)
    return list(employee_dicts)


def post(body):
    """Save an employee to the database."""
    if Employee.query.filter_by(id=body["id"]).first() is not None:
        return ("Employee already exists.", 400)
    employee = Employee.from_dict(body)
    db.session.add(employee)
    db.session.commit()


def get(id):
    """Get an employee from the database."""
    employee = Employee.query.filter_by(id=id).first()
    if employee is None:
        return ("Employee not found.", 404)
    return employee.to_dict()


def patch(body, id):
    """Update an employee in the dayabase."""
    employee = Employee.query.filter_by(id=id).first()
    if employee is None:
        return ("Employee not found.", 404)
    employee.name = body["name"]
    employee.division = body["division"]
    employee.salary = body["salary"]
    db.session.commit()
    return 200


def delete(id):
    """Delete an employee from the database."""
    result = Employee.query.filter_by(id=id).delete()
    if not result:
        return ("Employee not found.", 404)
    db.session.commit()
    return 200
