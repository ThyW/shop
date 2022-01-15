from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class App:
    def __init__(self, name: str) -> None:
        self._app = Flask(name, template_folder="templates")
        self._app.config["SQLALCHEMY_DATABASE_URI"] =\
                "postgresql://shop@localhost:5432/shop"
        self._db = SQLAlchemy(self._app)

    def get_flask(self) -> Flask:
        return self._app

    def get_db(self) -> SQLAlchemy:
        return self._db

    def run(self) -> None:
        return self._app.run()

