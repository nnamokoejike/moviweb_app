from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moviweb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # To suppress a warning
db = SQLAlchemy(app)
