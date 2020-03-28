from flask import render_template
from flask_classful import FlaskView, route

class MainView(FlaskView):
    trailing_slash = False
    
    @route('/')
    def index(self):

        return render_template("main/index.html")