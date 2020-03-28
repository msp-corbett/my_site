def register_routes(app):
    from app.frontend import register_routes as attach_frontend
    from app.api import register_routes as attach_api

    attach_frontend(app)
    attach_api(app)