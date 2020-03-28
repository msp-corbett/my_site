from .user import user_route
from .user.routes import UserView

PREFIX = '/api'

def register_routes(app):
    UserView.register(user_route, route_prefix=f'{PREFIX}')
    app.register_blueprint(user_route)