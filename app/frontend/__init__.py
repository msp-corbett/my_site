from .main import main_route
from .main.views import MainView

def register_routes(app):
    MainView.register(main_route, route_base='/')
    app.register_blueprint(main_route)