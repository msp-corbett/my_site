from sqlalchemy import exc, or_
from marshmallow import ValidationError
from flask import jsonify, request
from flask_classful import FlaskView, route
from app import db
from app.api.utils import APIError, BaseView
from .models import User, UserSchema


class UserView(BaseView):
    def __init__(self,):
        super().__init__()
        self.model = User
        self.schema = UserSchema
        self.update_filter = ['UserName', 'Email']
        # Use tablename, otherwise overwite this for messages.
        self.model_str = self.model.__tablename__

