import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import setup_db, Movie


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route("/", methods=["GET"])
    def index():
        movies = Movie.query.count()
        return jsonify({"status": "Healthy", "movies": movies})

    @app.route("/movies", methods=["POST"])
    def add_movie():
        movie = Movie("Lord of the Rings", "2005-05-25")
        movie.insert()
        return jsonify({"movie": movie.format()})

    @app.errorhandler(404)
    def error404(error):
        return jsonify({"error": "Not Found"}), 404

    return app


APP = create_app()

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)
