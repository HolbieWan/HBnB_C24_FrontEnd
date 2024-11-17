# route_users.py

from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity # type: ignore
from app.extensions import bcrypt


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# user_update_model = api.model('User_update', {
#     'first_name': fields.String(required=True, description='First name of the user'),
#     'last_name': fields.String(required=True, description='Last name of the user'),
#     'email': fields.String(required=True, description='Email of the user'),
# })

auth_header = {'Authorization': {
        'description': 'Bearer <JWT Token>',
        'in': 'header',
        'type': 'string',
        'required': True
    }
}


@api.route('/home')
class Home(Resource):
    """A protected endpoint that welcomes a logged-in user."""

    @api.doc('home', params=auth_header)
    @jwt_required()
    def get(self):
        """Returns a personalized welcome message for the logged-in user."""
        facade = current_app.extensions['FACADE']

        current_user = get_jwt_identity()
        current_user_id = current_user["id"]
        current_user = facade.get_user(current_user_id)
        current_user_first_name = current_user.first_name
        current_user_last_name = current_user.last_name

        return {"message": f"Hello {current_user_first_name} {current_user_last_name}"}, 200

@api.route('/')
class UserList(Resource):
    
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def post(self):
        """Register a new user"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        facade = current_app.extensions['FACADE']
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'password' : "****"
        }, 201
    
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        facade = current_app.extensions['FACADE']
        users = facade.get_all_users()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password' : "****"
            })
        return user_list, 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        facade = current_app.extensions['FACADE']
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password' : "****"
        }, 200
    
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def put(self, user_id):
        """Update a user's information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        facade = current_app.extensions['FACADE']

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        if not is_admin and user.id != current_user["id"]:
            return {'error': f'Unauthorized action, you can only modify your own data'}, 403

        user_data = api.payload
        new_password = user_data["password"]
        new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user_data["password"] = new_password

        if not is_admin:
            user_data["email"] = user.email
            user_data["password"] = user.password

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user and user.email != user_data['email']:
            return {'error': 'Email already registered'}, 400

        updated_user = facade.update_user(user_id, user_data)

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'password' : "****"
        }, 200
    
    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def delete(self, user_id):
        """Delete a user"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)

        facade = current_app.extensions['FACADE']
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        if not is_admin and user.id != current_user["id"]:
            return {'error': 'Unauthorized action, you can only modify your own data'}, 403

        facade.delete_user(user_id)
        return {'message': f'User {user_id} deleted successfully'}, 200
