from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autocommit": False, "autoflush": True})


def init_databases(app: Flask):
    db.init_app(app)
