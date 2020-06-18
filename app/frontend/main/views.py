from os import path
from flask import render_template, send_from_directory, current_app
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
    def login(self):
        """ Render the login form.

        Authentication and Authorisation handled by app.backend.auth
        """
        csrf.protect()
        context = {
            'form': LoginForm()}

        return render_template(
            "main/login.html",
            **context)

    @route('/signup')
    def signup(self):
        """ Render the login form.

        Authentication and Authorisation handled by app.backend.auth
        """
        csrf.protect()
        context = {
            'form': SignUpForm()}

        return render_template(
            "main/login.html",
            **context)

    @route('/favicon.ico')
    def favicon(self):
        return send_from_directory(
            path.join(
                current_app.root_path,
                'static'),
            'favicon.ico',)
