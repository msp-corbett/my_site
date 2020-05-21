from flask import render_template
from flask_classful import FlaskView, route
from flask_login import login_required
from app import csrf
from app.backend.auth.forms import LoginForm, SignUpForm

class MainView(FlaskView):
    trailing_slash = False

    decorators = []
    
    @route('/')
    @route('/home')
    def index(self):
        """ Site home page
        """

        return render_template(
            "main/index.html")


    @route('/login')
    @csrf.protect
    def login(self):
        """ Render the login form.

        Authentication and Authorisation handled by app.backend.auth
        """
        
        context = {
            'form': LoginForm()}

        return render_template(
            "main/login.html",
            **context)

    @route('/signup')
    @csrf.protect
    def signup(self):
        """ Render the login form.

        Authentication and Authorisation handled by app.backend.auth
        """
        
        context = {
            'form': SignUpForm()}

        return render_template(
            "main/login.html",
            **context)
