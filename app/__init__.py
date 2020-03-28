from flask import Flask, jsonify
from flask.wrappers import Response

def create_app(env: str = None) -> Flask:
    """ Flask Application Factory """

    from app.config import config_by_name
    
    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])

    @app.route("/health")
    def health() -> Response:
        """ Health check route """
        return jsonify("healthy"), 200

    return app
