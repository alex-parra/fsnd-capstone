from flask import jsonify


def setup_errors(app):
    """
    Apply error handlers to app
    """

    # Handle 400 Bad Request
    @app.errorhandler(400)
    def error400(error):
        msg = "bad request"
        return jsonify({"success": False, "error": 400, "message": msg}), 400

    # Handle 401 Unauthorized
    @app.errorhandler(401)
    def error401(error):
        msg = "unauthorized"
        return jsonify({"success": False, "error": 401, "message": msg}), 401

    # Handle 403 Forbidden
    @app.errorhandler(403)
    def error403(error):
        msg = "forbidden"
        return jsonify({"success": False, "error": 403, "message": msg}), 403

    # Handle 404 Not Found
    @app.errorhandler(404)
    def error404(error):
        msg = "not found"
        return jsonify({"success": False, "error": 404, "message": msg}), 404

    # Handle 422 unprocessable entity
    @app.errorhandler(422)
    def error422(error):
        msg = "unprocessable"
        return jsonify({"success": False, "error": 422, "message": msg}), 422

    # Handle 500 server error
    @app.errorhandler(500)
    def error500(error):
        msg = error.description
        return jsonify({"success": False, "error": 500, "message": msg}), 500
