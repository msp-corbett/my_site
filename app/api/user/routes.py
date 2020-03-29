from sqlalchemy import exc, or_
from marshmallow import ValidationError
from flask import jsonify, request
from flask_classful import FlaskView, route
from app import db
from .models import User, UserSchema


class UserView(FlaskView):
    trailing_slash = False

    @route('')
    @route('/<int:pk_id>')
    def get(self, pk_id=None):
        if pk_id:
            schema = UserSchema()
            data = db.session.query(User).filter((User.ID == pk_id)).first()
        else:
            schema = UserSchema(many=True)
            data = db.session.query(User).all()
        
        return schema.jsonify(data)


    def post(self,):
        schema = UserSchema()
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        try:
            data = schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        user_name, email = data["UserName"], data["Email"]
        
        user = db.session.\
            query(
                User).\
            filter(
                or_(
                    (User.Email == email),
                    (User.UserName == user_name))).\
            first()
        
        if user is None:
            user = User(
                FirstName=data['FirstName'],
                LastName=data['LastName'],
                UserName=user_name,
                Email=email)
            try:
                db.session.add(user)
                db.session.commit()
                data, response = {"message": f"Created user: {user_name}"}, 200
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                data, response = {"message": f"Could not create uesr: {user_name} with email: {email}."}, 200
        else:
            data, response = {"message": f"User with {user_name} or {email} already exists."}, 200

        return data, response


    def put(self,):
        pass


    def patch(self, pk_id):
        pass


    def delete(self): 
        pass

