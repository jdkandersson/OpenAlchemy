"""Application code."""

import connexion

from models import db

app = connexion.FlaskApp(__name__, specification_dir=".")
app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db.init_app(app.app)
with app.app.app_context():
    db.create_all()
app.add_api("api.yaml")
app.run(port=8080)
