from flask import jsonify
from flask_classful import FlaskView, route
from app import db
from .models import User, UserSchema

users = [
    {
        'id': 1,
        'name': 'Michael',
        'email': 'm@mysite.com'
    },
    {
        'id': 2,
        'name': 'Jimmy',
        'email': 'j@mysite.com'
    }
]

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
        pass


    def put(self,):
        pass


    def patch(self, pk_id):
        pass


    def delete(self): 
        pass

