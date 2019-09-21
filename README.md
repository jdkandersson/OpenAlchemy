# openapi-SQLAlchemy
Translates an openapi schema to SQLAlchemy models.

## Installation
```bash
python3 -m pip install openapi-SQLAlchemy
# To be able to load yaml file
python3 -m pip install PyYAML
```

## Example

For example, given the following openapi specification:

```yaml
# example-spec.yml
openapi: "3.0.0"

info:
  title: Test Schema
  description: API to illustrate openapi-SQLALchemy MVP.
  version: "0.1"

paths:
  /employee:
    get:
      summary: Used to retrieve all employees.
      responses:
        200:
          description: Return all employees from the database.
          content:
            application/json:
              schema:
                type: array
                items:
                  "$ref": "#/components/schemas/Employee"

components:
  schemas:
    Employee:
      description: Person that works for a company.
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          description: Unique identifier for the employee.
          example: 0
          x-primary-key: true
          x-autoincrement: true
        name:
          type: string
          description: The name of the employee.
          example: David Andersson.
          x-index: true
        division:
          type: string
          description: The part of the company the employee works in.
          example: Engineering
          x-index: true
        salary:
          type: number
          description: The amount of money the employee is paid.
          example: 1000000.00
      required:
        - id
        - name
        - division
```

The SQLALchemy models file then becomes:
```python
# models.py
from yaml import load, Loader
from sqlalchemy.ext.declarative import declarative_base
from openapi_sqlalchemy import init_model_factory


Base = declarative_base()
with open("example-spec.yml") as spec_file:
    SPEC = load(spec_file, Loader=Loader)
MODEL_FACTORY = init_model_factory(base=Base, spec=SPEC)


Employee = MODEL_FACTORY(name="Employee")

```

## Documentation
[Read the Docs](https://openapi-sqlalchemy.readthedocs.io/en/latest/)

## Features
### Supported
The following features are supported:
- `integer ` (32 and 64 bit),
- `number` (float only),
- `boolean`,
- `string`,
- `$ref` references for columns,
- foreign keys,
- many to one relationships and
- `allOf` inheritance for columns.

### Not Supported
The following features are on the backlog:
- `allOf` inheritance for models,
- `$ref` references for models and
- one to many relationships.

## Contributing
Fork and checkout the repository. To install:
```bash
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -e .[dev]
```
To run tests:
```bash
tox
```
Make your changes and raise a pull request.

## Compiling Docs
```bash
python3 -m venv venv
cd docs
make html
```
This creates the `index.html` file in `docs/build/html/index.html`.
