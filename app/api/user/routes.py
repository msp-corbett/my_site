from sqlalchemy import exc, or_
from marshmallow import ValidationError
from flask import jsonify, request
from flask_classful import FlaskView, route
from app import db
from .models import User, UserSchema


class UserView(FlaskView):
    trailing_slash = False

    def index(self,):
        schema = UserSchema(many=True)
        data = db.session.query(User).all()
        return schema.jsonify(data)


    def get(self, pk_id):
        schema = UserSchema()
        data = db.session.query(User).filter((User.ID == pk_id)).first()
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


    def put(self, pk_id):
        """ PUT not supported on model that generates incremental Primary Key """
        return {"message": "method not allowed."}, 405

    
    def patch(self, pk_id):
        record_query = db.session.query(User).filter((User.ID == pk_id)).first()
        schema = UserSchema()

        # User agent should know target resource via GET request.
        if not record_query:
            return {"message": "Requested user not found"}, 404
        
        request_data = request.get_json(force=True, silent=True)
        if not request_data:
            return {'message': 'No content provided.'}, 400

        # Build patch from supplied data
        apply_patch = {}
        allowed_operations = ("replace")
        for patch_data in request_data:
            try:
                if patch_data.get("op").lower() not in allowed_operations:
                    return {'message': f'Operation "{patch_data.get("op")}" not supported.'}, 400
            except AttributeError:
                return {'message': f'Invalid operation {patch_data.get("op")}.'}, 400

            apply_patch.update({patch_data.get('path'): patch_data.get("value")})

        # Validate request data
        try:
            schema.load(apply_patch)
        except ValidationError as err:
            return {'message': err.messages}, 400

        try:
            for k, v in apply_patch.items():
                setattr(record_query, k, v)
            db.session.commit()
            data, code = {'message': f"User updated."}, 200
        except (exc.SQLAlchemyError, TypeError):
            db.session.rollback()
            data, code = {"message": "Record could not be updated."}, 500

        return data, code

    
    def delete(self, pk_id): 
        user = db.session.query(User).filter((User.ID == pk_id)).first()

        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                data, response = {"message": "record deleted."}, 200
            except exc.SQLAlchemyError:
                db.session.rollback()
                data, response = {"message": "Record could not be deleted."}, 500
        else:
            data, response = {"message": "No matching user."}, 404
        
        return data, response

