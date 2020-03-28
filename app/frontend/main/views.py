from flask import render_template
from flask_classful import FlaskView

class MainView(FlaskView):
    trailing_slash = False
    
    def index(self):

        return render_template("main/index.html")