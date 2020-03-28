from flask import Blueprint
from .views import MainView

main_route = Blueprint('main', __name__, template_folder='templates')
