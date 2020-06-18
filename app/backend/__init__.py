from .auth import auth_route
from .auth.routes import AuthView

def register_routes(app):
    AuthView.register(auth_route, route_base='/auth')
    app.register_blueprint(auth_route)
