import os
from flask import request, abort, jsonify, request, render_template
from .config import BASE_URL
from .models import Movie, Actor
from .auth import requires_auth, login_url, get_permissions


def setup_routes(app):
    """Applies routes to app"""

    @app.route("/", methods=["GET"])
    def index():
        data = {"app_url": BASE_URL, "login_url": login_url(), "api_url": BASE_URL}
        return render_template("index.html", **data)

    @app.route("/health", methods=["GET"])
    def healthcheck():
        data = {
            "status": "Healthy",
            "movies": Movie.query.count(),
            "actors": Actor.query.count(),
            "auth": {"domain": os.environ.get("AUTH_DOMAIN")},
        }
        return jsonify(data)

    @app.route("/user", methods=["GET"])
    @requires_auth()
    def get_user(jwt):
        return jsonify({"permissions": get_permissions()})

    # ------------------------------------------------------------
    # Movies
    @app.route("/movies", methods=["GET"])
    @requires_auth("movies:list")
    def get_movies(jwt):
        """GET /movies - List all movies"""
        movies = Movie.query.all()
        return jsonify({"movies": [m.data() for m in movies]})

    @app.route("/movies", methods=["POST"])
    @requires_auth("movies:create")
    def add_movie(jwt):
        """POST /movies - Create new movie"""
        data = request.get_json(force=True)
        exists = Movie.query.filter(Movie.title == data["title"]).count()
        if exists:
            abort(405)

        movie = Movie(**data)
        movie.insert()
        return jsonify({"movie": movie.data()})

    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth("movies:update")
    def update_movie(jwt, id):
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
    @requires_auth("movies:delete")
    def delete_movie(jwt, id):
        """DELETE /movies/:id - Delete a movie"""
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({"deleted": movie.data()}), 204

    # ------------------------------------------------------------
    # Actors
    @app.route("/actors", methods=["GET"])
    @requires_auth("actors:list")
    def get_actors(jwt):
        """GET /actors - List all actors"""
        actors = Actor.query.all()
        return jsonify({"actors": [a.data() for a in actors]})

    @app.route("/actors", methods=["POST"])
    @requires_auth("actors:create")
    def add_actor(jwt):
        """POST /actors - Create a new actor"""
        data = request.get_json(force=True)
        exists = Actor.query.filter(Actor.name == data["name"]).count()
        if exists:
            abort(405)

        actor = Actor(**data)
        actor.insert()
        return jsonify({"actor": actor.data()})

    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth("actors:update")
    def update_actor(jwt, id):
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
    @requires_auth("actors:delete")
    def delete_actor(jwt, id):
        """DELETE /actors/:id - Delete an actor"""
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({"deleted": actor.data()}), 204
