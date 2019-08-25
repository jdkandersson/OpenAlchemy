from sqlalchemy.ext.declarative import declarative_base
from yaml import Loader
from yaml import load

from openapi_sqlalchemy import init_model_factory

Base = declarative_base()
with open("simple-example-spec.yml") as spec_file:
    SPEC = load(spec_file, Loader=Loader)
MODEL_FACTORY = init_model_factory(base=Base, spec=SPEC)


Employee = MODEL_FACTORY(name="Employee")
