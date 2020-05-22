from flask import request, abort, jsonify
from .models import Movie


def setup_routes(app):
    """Applies routes to app"""

    @app.route("/", methods=["GET"])
    def index():
        movies = Movie.query.count()
        return jsonify({"status": "Healthy", "movies": movies})

    @app.route("/movies", methods=["POST"])
    def add_movie():
        movie = Movie("Lord of the Rings", "2005-05-25")
        movie.insert()
        return jsonify({"movie": movie.format()})
