from enum import unique
import os
import connexion
# from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

# Creating the app instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Config
app.config["JSON_SORT_KEYS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alarms2.db"
