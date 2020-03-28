from flask import Flask, jsonify
from flask.wrappers import Response

def create_app() -> Flask:
    """ Flask Application Factory """

    app = Flask(__name__)

    @app.route("/health")
    def health() -> Response:
        """ Health check route """
        return jsonify("healthly"), 200

    return app
