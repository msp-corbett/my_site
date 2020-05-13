from sqlalchemy import exc, or_
from marshmallow import ValidationError
from flask import jsonify, request
from flask_classful import FlaskView, route
from app import db
from app.api.utils import APIError, ApiView
from .models import (
    Widget, Fizzler, Banger,
    WidgetSchema, FizzlerSchema, BangerSchema)


class WidgetView(ApiView):
    def __init__(self,):
        super().__init__()
        self.model = Widget
        self.schema = WidgetSchema
        self.update_filter = ['Name']
        # Use tablename, otherwise overwite this for messages.
        self.model_str = self.model.__tablename__


class FizzlerView(ApiView):
    def __init__(self,):
        super().__init__()
        self.model = Fizzler
        self.schema = FizzlerSchema
        self.update_filter = ['Name']
        # Use tablename, otherwise overwite this for messages.
        self.model_str = self.model.__tablename__


class BangerView(ApiView):
    def __init__(self,):
        super().__init__()
        self.model = Banger
        self.schema = BangerSchema
        self.update_filter = ['Name']
        # Use tablename, otherwise overwite this for messages.
        self.model_str = self.model.__tablename__