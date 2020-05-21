from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    UserName = StringField(
        'User name',
        validators=[InputRequired()])
    Password = PasswordField(
        'Password',
        validators=[InputRequired()])


class SignUpForm(FlaskForm):
    FirstName = StringField(
        'Name',
        validators=[InputRequired()])
    LastName = StringField(
        'Surname',
        validators=[InputRequired()])
    Email = StringField(
        'Email',
        validators=[InputRequired(), Email()])
    UserName = StringField(
        'User name',
        validators=[InputRequired()])
    Password = PasswordField(
        'Password',
        validators=[InputRequired()])