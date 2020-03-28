def register_routes(app):
    from app.frontend import register_routes as attach_frontend

    attach_frontend(app)