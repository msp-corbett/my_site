from .user import user_route
from .user.routes import UserView
from .widget import widget_route
from .widget.routes import WidgetView, FizzlerView, BangerView

PREFIX = '/api'

def register_routes(app):
    UserView.register(user_route, route_prefix=f'{PREFIX}')
    app.register_blueprint(user_route)


    WidgetView.register(widget_route)
    FizzlerView.register(widget_route)
    BangerView.register(widget_route)
    app.register_blueprint(widget_route)