from flask import jsonify
from .auth import AuthError
import jsonschema


def setup_errors(app):
    """
    Apply error handlers to app
    """

    # Handle 400 Bad Request
    @app.errorhandler(400)
    def error400(error):
        msg = "Bad Request"
        return jsonify({"success": False, "error": 400, "message": msg}), 400

    # Handle 401 Unauthorized
    @app.errorhandler(401)
    def error401(error):
        msg = "Unauthorized"
        return jsonify({"success": False, "error": 401, "message": msg}), 401

    # Handle 403 Forbidden
    @app.errorhandler(403)
    def error403(error):
        msg = "Forbidden"
        return jsonify({"success": False, "error": 403, "message": msg}), 403

    # Handle AuthError
    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        code = error.status_code
        msg = error.error
        return jsonify({"success": False, "error": code, "msg": msg}), code

    # Handle 404 Not Found
    @app.errorhandler(404)
    def error404(error):
        msg = "Not Found"
        return jsonify({"success": False, "error": 404, "message": msg}), 404

    # Handle 405 Not Allowed
    @app.errorhandler(405)
    def error405(error):
        msg = "Not Allowed"
        return jsonify({"success": False, "error": 405, "message": msg}), 405

    # Handle 422 Unprocessable Entity
    @app.errorhandler(422)
    def error422(error):
        msg = "Unprocessable"
        return jsonify({"success": False, "error": 422, "message": msg}), 422

    # Handle 500 server error
    @app.errorhandler(500)
    def error500(error):
        msg = error.description
        return jsonify({"success": False, "error": 500, "message": msg}), 500

    # Handle Validation Error
    @app.errorhandler(jsonschema.ValidationError)
    def onValidationError(e):
        return jsonify({"success": False, "error": 400, "message": "There was a validation error: " + str(e)}), 400
