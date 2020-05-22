import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

DB_PATH = f"postgres://postgres:123456@localhost:5432/capstone"
DB_URL = os.environ.get("DATABASE_URL", DB_PATH)

db = SQLAlchemy()


def setup_db(app, database_path=DB_URL):
    """binds a flask application and a SQLAlchemy service"""
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
        - data
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

    def data(self):
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


class Actor(db.Model):
    """
    Actor Model
        Attributes:
        - name: string
        - age: int
        - gender: M | F | X
        Methods:
        - data
        - insert
        - update
        - delete
    """

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
