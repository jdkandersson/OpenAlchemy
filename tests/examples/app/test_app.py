"""Tests for example app."""

import json

import pytest

from examples.app import models


@pytest.mark.app
def test_post(client, db_session):
    """
    GIVEN employee
    WHEN /employee POST is called with the employee
    THEN the employee is in the database.
    """
    employee = {"id": 1, "name": "name 1", "division": "division 1", "salary": 1.0}

    response = client.post(
        "/employee",
        data=json.dumps(employee),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    db_employees = db_session.query(models.Employee).all()
    assert len(db_employees) == 1
    db_employee = db_employees[0]
    assert db_employee.id == employee["id"]
    assert db_employee.name == employee["name"]
    assert db_employee.division == employee["division"]
    assert db_employee.salary == employee["salary"]


@pytest.mark.app
def test_post_duplicate(client):
    """
    GIVEN employee
    WHEN /employee POST is called twice with the employee
    THEN 400 is returned.
    """
    employee = {"id": 1, "name": "name 1", "division": "division 1", "salary": 1.0}

    client.post(
        "/employee",
        data=json.dumps(employee),
        headers={"Content-Type": "application/json"},
    )
    response = client.post(
        "/employee",
        data=json.dumps(employee),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400


@pytest.mark.app
def test_get(client, db_session):
    """
    GIVEN database with employee
    WHEN /employee GET is called
    THEN the employee is returned.
    """
    db_employee = models.Employee(
        id=1, name="name 1", division="division 1", salary=1.0
    )
    db_session.add(db_employee)
    db_session.flush()

    response = client.get("/employee")

    assert response.status_code == 200
    employees = response.json
    assert len(employees) == 1
    employee = employees[0]
    assert employee["id"] == db_employee.id
    assert employee["name"] == db_employee.name
    assert employee["division"] == db_employee.division
    assert employee["salary"] == db_employee.salary


@pytest.mark.app
def test_get_id_miss(client, db_session):
    """
    GIVEN database with employee
    WHEN /employee/{id} GET is called with a different id
    THEN 404 is returned.
    """
    db_employee = models.Employee(
        id=1, name="name 1", division="division 1", salary=1.0
    )
    db_session.add(db_employee)
    db_session.flush()

    response = client.get("/employee/2")

    assert response.status_code == 404


@pytest.mark.app
def test_get_id_hit(client, db_session):
    """
    GIVEN database with employee
    WHEN /employee/{id} GET is called with the id of the employee
    THEN the employee is returned.
    """
    db_employee = models.Employee(
        id=1, name="name 1", division="division 1", salary=1.0
    )
    db_session.add(db_employee)
    db_session.flush()

    response = client.get(f"/employee/{db_employee.id}")

    assert response.status_code == 200
    employee = response.json
    assert employee["id"] == db_employee.id
    assert employee["name"] == db_employee.name
    assert employee["division"] == db_employee.division
    assert employee["salary"] == db_employee.salary


@pytest.mark.app
def test_patch_id_miss(client, db_session):
    """
    GIVEN database with employee
    WHEN /employee/{id} PATCH is called with a different id
    THEN 404 is returned.
    """
    db_employee = models.Employee(
        id=1, name="name 1", division="division 1", salary=1.0
    )
    db_session.add(db_employee)
    db_session.flush()
    employee = {"id": 2, "name": "name 2", "division": "division 2", "salary": 2.0}

    response = client.patch(
        "/employee/2",
        data=json.dumps(employee),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 404


@pytest.mark.app
def test_patch_id_hit(client, db_session):
    """
    GIVEN database with employee
    WHEN /employee/{id} PATCH is called with the id of the employee
    THEN the employee is updated.
    """
    db_employee = models.Employee(
        id=1, name="name 1", division="division 1", salary=1.0
    )
    db_session.add(db_employee)
    db_session.flush()
    employee = {
        "id": db_employee.id,
        "name": "name 2",
        "division": "division 2",
        "salary": 2.0,
    }

    response = client.patch(
        f"/employee/{db_employee.id}",
        data=json.dumps(employee),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    db_session.refresh(db_employee)
    assert db_employee.id == employee["id"]
    assert db_employee.name == employee["name"]
    assert db_employee.division == employee["division"]
    assert db_employee.salary == employee["salary"]


@pytest.mark.app
def test_delete_id_miss(client, db_session):
    """
    GIVEN database with employee
    WHEN /employee/{id} DELETE is called with a different id
    THEN 404 is returned.
    """
    db_employee = models.Employee(
        id=1, name="name 1", division="division 1", salary=1.0
    )
    db_session.add(db_employee)
    db_session.flush()

    response = client.delete("/employee/2")

    assert response.status_code == 404


@pytest.mark.app
def test_delete_id_hit(client, db_session):
    """
    GIVEN database with employee
    WHEN /employee/{id} DELETE is called with the id of the employee
    THEN the employee is updated.
    """
    db_employee = models.Employee(
        id=1, name="name 1", division="division 1", salary=1.0
    )
    db_session.add(db_employee)
    db_session.flush()

    response = client.delete(f"/employee/{db_employee.id}")

    assert response.status_code == 200
    db_employees = db_session.query(models.Employee).all()
    assert len(db_employees) == 0
