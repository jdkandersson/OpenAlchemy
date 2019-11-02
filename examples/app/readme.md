# Connexion App

To start the app:
```python
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

To see the UI go to:
[Swagger UI](http://localhost:8080/ui/)

The OpenAPI specification has been defined in the [api.yaml](api.yaml) file.
The database is configured in the [database.py](database.py) file. The
endpoint fulfillment functions are defined in the [api.py](api.py) file. The
API configuration has been defined in the [app.py](app.py) file.
