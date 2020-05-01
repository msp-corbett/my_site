from sqlalchemy import exc, or_
from marshmallow import ValidationError
from flask import jsonify, request, Response
from flask_classful import FlaskView, route
from app import db

class APIError(Exception):
    """ Exception to raise when API call errors

    Attributes:
        error_code -- HTML response error code to pass back.
        error_source -- value where the error occured.
    """

    def __init__(self, error_code, error_source):
        self.error_code = error_code
        self.error_source = error_source


class ApiView(FlaskView):
    trailing_slash = False

    def __init__(self,):
        super().__init__()
        self.model = None
        self.schema = None
        # Unique filters to check, Post, Put and Patch requets
        self.update_filter = None 
        # Use tablename, otherwise overwite this for messages.
        self.model_str = None

    
    def filter_query(self, query, raw_filters):
        """
            Modified version of accpeted answer from:
            https://stackoverflow.com/questions/14845196/dynamically-constructing-filters-in-sqlalchemy

            1 - Split the desired filters out from filters url argument
            2 - split each filter into the Column corresponding to the Model.Column, the filter operator and the search value
            3 - using a lambda funciton create corresponding SQLAlchemy ORM Internal
            - https://docs.sqlalchemy.org/en/13/orm/internals.html
            4 - Create and chain the filter(s) to the query.

            Example:
            import requests
            r = requests.get('http://server/api/user?filters=FirstName eq "Jimmy" AND LastName eq "Bob")
        """

        for filter_ in raw_filters.split(' AND '):
            try:
                key, op, value = filter_.split(' ', maxsplit=2)
            except ValueError:
                raise APIError(400, f'Invalid filter: {filter_}')

            value = value.strip("'")
            value = value.strip('"')

            column = getattr(self.model, key, None)
            if not column:
                raise APIError(400, f'Invalid field: {key}')

            if op == 'in':
                values = value.split(',')
                values = [v.strip(' ') for v in values]
                filt = column.in_(values)
            else:
                try:
                    attr = list(filter(lambda e: hasattr(column, f"{e}"), [f'{op}', f'{op}_', f'__{op}__']))[0]
                except IndexError:
                    raise APIError(400, f'Invalid operation: {op}')
                if value == 'null':
                    value = None

            filt = getattr(column, attr)(value)
            query = query.filter(filt)
        return query


    def unq_filter(self, filter_dict: dict):
        """ Create a single or set of filter for Unique fields on a model.

        Keyword Arguments;

        filter_dict: contains Model Column and value in key:value pair.

        If there are mulitple Unqiue fields, will return tuple in 
        
        """
        _return_filter = []
        for key,value in filter_dict.items():
            column = getattr(self.model, key)
            _filter = getattr(column, '__eq__')(value)
            _return_filter.append(_filter)
        
        if not _return_filter:
            # Always True filter to return if filter_dict fails to produce a filter
            _return_filter = (1 == 1)
        else:
            # Create an SQL 'OR' Filter for multiple fields 
            if len(_return_filter) > 1:
                _return_filter = or_(*_return_filter)
        
        return _return_filter


    def index(self,) -> Response:
        """ Index route to provide list of Users """
        args = {
            'filters': request.args.get('filters', ''),
            'pageSize': request.args.get('pageSize', 25),
            'page': request.args.get('page', 1)
        }

        if args['filters']:
            try:
                data = self.filter_query(
                    query=db.session.query(self.model),
                    raw_filters=args['filters'])
            except APIError as err:
                return {"message": err.error_source}, err.error_code
        else:
            data = db.session.query(self.model)
                
        return self.schema(many=True).jsonify(data)


    def get(self, pk_id: int) -> Response:
        """ Get method to retrieve specific record.
        
        Keyword arguments:
        pk_id -- Primary Key value of Model

        """
        data = db.session.query(self.model).filter((self.model.ID == pk_id)).first()
        
        return self.schema().jsonify(data)


    def post(self,) -> Response:
        """ POST method to create record. """

        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        try:
            data = self.schema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        update_dict = {f"{f}": data[f] for f in self.update_filter}
        _unq_filter = self.unq_filter(update_dict)

        record = db.session.\
            query(
                self.model).\
            filter(
                _unq_filter ).\
            first()
        
        if record is None:
            record = self.model(
                **data)
            try:
                db.session.add(record)
                db.session.commit()
                data, response = {"message": f"Created {self.model_str}"}, 200
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                data, response = {"message": f"Could not create {self.model_str}"}, 200
        else:
            data, response = {"message": f"{self.model_str} already exists."}, 200

        return data, response


    def put(self, pk_id):
        """ PUT method to Update entire Record

        Keyword arguments:
        pk_id -- Primary Key value of record Model

        Note: Primary Key is created by Database Sequence, therefore
        PUT method only works when record already exists.
        Similar functionality to PATCH, but whole record needs to be
        sent in request.
        
        """

        record_query = db.session.query(self.model).get(pk_id)
        
        # User agent should know target resource via GET request.
        if not record_query:
            return {"message": "Record not found"}, 404

        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        try:
            data = self.schema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        try:
            for k, v in data.items():
                setattr(record_query, k, v)
            db.session.commit()
            data, code = {'message': f"{self.model_str} updated."}, 200
        except (exc.SQLAlchemyError, TypeError):
            db.session.rollback()
            data, code = {"message": f"{self.model_str} record could not be updated."}, 500

        return data, code
        

    
    def patch(self, pk_id):
        """ Patch method to update part(s) of record model.

        Keyword arguments:
        pk_id -- Primary Key value of record Model

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

        Update occurs similiary to PUT method, however patch doesn't require
        whole record in request.  Allows for reduce bandwidth requests for larger models.
        """
        record_query = db.session.query(self.model).filter((self.model.ID == pk_id)).first()

        # User agent should know target resource via GET request.
        if not record_query:
            return {"message": "Record not found"}, 404
        
        request_data = request.get_json(force=True, silent=True)
        if not request_data:
            return {'message': 'No content provided.'}, 400

        # Build patch from supplied data
        apply_patch = {}
        allowed_operations = ("replace",)
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
        """ Delete method to remove specific record.
        
        Keyword arguments:
        pk_id -- Primary Key value of Model

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

