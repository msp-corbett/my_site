from flask import Flask, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app(env: str = None) -> Flask:
    """ Flask Application Factory """

    from app.config import config_by_name
    from app.routes import register_routes
    
    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])

    db.init_app(app)

    ma.init_app(app)

    register_routes(app)

    @app.route("/health")
    def health() -> Response:
        """ Health check route """
        return jsonify("healthy"), 200

    return app
