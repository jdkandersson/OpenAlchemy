from openapi_sqlalchemy import init_yaml

Base, model_factory = init_yaml("ref-model-example-spec.yml")

Employee = model_factory(name="Employee")
