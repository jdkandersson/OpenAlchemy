from openapi_sqlalchemy import init_yaml

Base, model_factory = init_yaml("simple-example-spec.yml")

Employee = model_factory(name="Employee")
