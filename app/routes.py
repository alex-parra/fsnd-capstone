from flask import request, abort, jsonify
from .models import Movie, Actor


def setup_routes(app):
    """Applies routes to app"""

    @app.route("/", methods=["GET"])
    def index():
        data = {
            "status": "Healthy",
            "movies": Movie.query.count(),
            "actors": Actor.query.count(),
        }
        return jsonify(data)

    # ------------------------------------------------------------
    # Movies
    @app.route("/movies", methods=["GET"])
    def get_movies():
        """GET /movies - List all movies"""
        movies = Movie.query.all()
        return jsonify({"movies": [m.data() for m in movies]})

    @app.route("/movies", methods=["POST"])
    def add_movie():
        """POST /movies - Create new movie"""
        data = request.get_json(force=True)
        exists = Movie.query.filter(Movie.title == data["title"]).count()
        if exists:
            abort(405)

        movie = Movie(**data)
        movie.insert()
        return jsonify({"movie": movie.data()})

    @app.route("/movies/<int:id>", methods=["PATCH"])
    def update_movie(id):
        """PATCH /movies/:id - Update a movie"""
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)

        data = request.get_json(force=True)
        movie.title = data.get("title", movie.title)
        movie.release_date = data.get("release_date", movie.release_date)
        movie.update()
        return jsonify({"movie": movie.data()})

    @app.route("/movies/<int:id>", methods=["DELETE"])
    def delete_movie(id):
        """DELETE /movies/:id - Delete a movie"""
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({"deleted": movie.data()}), 204

    # ------------------------------------------------------------
    # Actors
    @app.route("/actors", methods=["GET"])
    def get_actors():
        """GET /actors - List all actors"""
        actors = Actor.query.all()
        return jsonify({"actors": [a.data() for a in actors]})

    @app.route("/actors", methods=["POST"])
    def add_actor():
        """POST /actors - Create a new actor"""
        data = request.get_json(force=True)
        exists = Actor.query.filter(Actor.name == data["name"]).count()
        if exists:
            abort(405)

        actor = Actor(**data)
        actor.insert()
        return jsonify({"actor": actor.data()})

    @app.route("/actors/<int:id>", methods=["PATCH"])
    def update_actor(id):
        """PATCH /actors/:id - Update an actor"""
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)

        data = request.get_json(force=True)
        actor.name = data.get("name", actor.name)
        actor.age = data.get("age", actor.age)
        actor.gender = data.get("gender", actor.gender)
        actor.update()
        return jsonify({"actor": actor.data()})

    @app.route("/actors/<int:id>", methods=["DELETE"])
    def delete_actor(id):
        """DELETE /actors/:id - Delete an actor"""
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({"deleted": actor.data()}), 204
