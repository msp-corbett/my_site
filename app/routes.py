def register_routes(app):
    from app.frontend import register_routes as attach_frontend
    from app.backend import register_routes as attach_backend
    from app.api import register_routes as attach_api

    attach_frontend(app)
    attach_backend(app)
    attach_api(app)

