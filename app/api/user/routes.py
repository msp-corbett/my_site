from sqlalchemy import exc, or_
from marshmallow import ValidationError
from flask import jsonify, request
from flask_classful import FlaskView, route
from app import db
from app.api.utils import APIError, filter_query
from .models import User, UserSchema

#TODO add type hints

class UserView(FlaskView):
    trailing_slash = False

    def __init__(self,):
        super().__init__()
        self.model = User
        self.schema = UserSchema
        self.update_filter = ['UserName', 'Email']
        # Use tablename, otherwise overwite this for messages.
        self.model_str = self.model.__tablename__


    def index(self, ):
        """ Index route to provide list of Users """
        args = {
            'filters': request.args.get('filters', ''),
            'pageSize': request.args.get('pageSize', 25),
            'page': request.args.get('page', 1)
        }
        if args['filters']:
            try:
                data = filter_query(
                    query=db.session.query(self.model),
                    raw_filters=args['filters'],
                    model=self.model)
            except APIError as err:
                return {"message": err.error_source}, err.error_code
        else:
            data = db.session.query(self.model)
                
        return self.schema(many=True).jsonify(data)


    def get(self, pk_id):
        """ Get method to retrieve specific user.
        
        Keyword arguments:
        pk_id -- Primary Key value of User Model

        """
        data = db.session.query(self.model).filter((self.model.ID == pk_id)).first()
        
        return self.schema().jsonify(data)


    def post(self,):
        """ POST method to create user record. """

        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        try:
            data = self.schema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        # Filter on unique fields
        if self.update_filter:
            for f in self.update_filter:
                _filter = (getattr(self.model, f) == data[f])

        user_name, email = data["UserName"], data["Email"]
        
        record = db.session.\
            query(
                self.model).\
            filter(
                self.update_filter).\
            first()
        
        if record is None:
            record = self.model(
                **data)
            try:
                db.session.add(record)
                db.session.commit()
                data, response = {"message": f"Created {self.model_str}: {user_name}"}, 200
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                data, response = {"message": f"Could not create {self.model_str}: {user_name}."}, 200
        else:
            data, response = {"message": f"{self.model_str} with {user_name} or {email} already exists."}, 200

        return data, response


    def put(self, pk_id):
        """ PUT not supported on model that generates incremental Primary Key """
        #TODO Allow method only if record already exists.

        return {"message": "method not allowed."}, 405

    
    def patch(self, pk_id):
        """ Patch method to update part(s) of User model.

        Keyword arguments:
        pk_id -- Primary Key value of User Model

        Inspired by ConnectWise API.
        Patch body needs to be an array containing dict(s) of update instruction.
        Example:
            import requests
            patch = [
                {
                    'op': 'replace',
                    'path': 'FirstName',
                    'value': 'Jimmy'
                }
            ]

            requets.patch('http://server/api/user/1', json=patch)

        """
        record_query = db.session.query(self.model).filter((self.model.ID == pk_id)).first()

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
            self.schema().load(apply_patch)
        except ValidationError as err:
            return {'message': err.messages}, 400

        try:
            for k, v in apply_patch.items():
                setattr(record_query, k, v)
            db.session.commit()
            data, code = {'message': f"{self.model_str} updated."}, 200
        except (exc.SQLAlchemyError, TypeError):
            db.session.rollback()
            data, code = {"message": f"{self.model_str} record could not be updated."}, 500

        return data, code

    
    def delete(self, pk_id): 
        """ Delete method to remove specific user.
        
        Keyword arguments:
        pk_id -- Primary Key value of User Model

        """
        record = db.session.query(self.model).filter((self.model.ID == pk_id)).first()

        if record:
            try:
                db.session.delete(record)
                db.session.commit()
                data, response = {"message": f"{self.model_str} record deleted."}, 200
            except exc.SQLAlchemyError:
                db.session.rollback()
                data, response = {"message": f"{self.model_str} record could not be deleted."}, 500
        else:
            data, response = {"message": f"No matching {self.model_str} record."}, 404
        
        return data, response

