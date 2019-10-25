from openapi_sqlalchemy import init_yaml

_, model_factory = init_yaml("all-of-column-example-spec.yml")


Division = model_factory(name="Division")
Employee = model_factory(name="Employee")
