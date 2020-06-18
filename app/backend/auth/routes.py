from flask import url_for, redirect
from flask_classful import FlaskView, route
from flask_login import current_user
from app import db, login, csrf
from app.api.user.models import User
from .forms import LoginForm, SignUpForm

class AuthView(FlaskView):
    trailing_slash = False
    excluded_methods = ['user_loader']

    @login.user_loader
    def user_loader(self, user_name:str) -> User:
        """ Flask-Login requirement

        Given a user_name, return the User object.

        Keyword args:

        user_name str: User.UserName to retrieve.
        """

        user = db.session.\
            query(
                User).\
            filter(
                User.UserName == user_name).\
            first()

        return user

    @route('/login', methods=['POST'])
    def login(self,):
        csrf.protect()
        if current_user.is_authenticated:
            return redirect(url_for("main.MainView:login"))

        form = LoginForm()
        if form.validate_on_submit():
            pass
            #TODO check user password
            #Log user in
        
        return redirect(url_for("main.MainView:index"))


    @route('/logout')
    def logout(self,):
        pass
        #TODO clear current_user


    @route('/signup', methods=['POST'])
    def signup(self,):
        csrf.protect()
        form = SignUpForm()

        if form.validate_on_submit():
            pass
            # TODO Create User object
            # Log User in

        return redirect(url_for("main.MainView:index"))