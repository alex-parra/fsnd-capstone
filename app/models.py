import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

DB_NAME = "capstone"
DB_HOST = "localhost:5432"
DB_USER = "postgres:123456"
DB_PATH = f"postgres://{DB_USER}@{DB_HOST}/{DB_NAME}"

db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    Migrate(app, db)


class Movie(db.Model):
    """
    Movie Model
        Attributes:
        - title: string
        - release_date: string
        Methods:
        - insert
        - update
        - delete
    """

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
