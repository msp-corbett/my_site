from flask import jsonify
from flask_classful import FlaskView, route

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
            data, response = next((user for user in users if user.get('id') == pk_id), {'Error': 'User does not exist.'}), 200
        else:
            data, response = users, 200
        
        return jsonify(data), response


    def post(self,):
        pass


    def put(self,):
        pass


    def patch(self, pk_id):
        pass


    def delete(self): 
        pass

