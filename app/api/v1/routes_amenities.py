from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity # type: ignore


api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

auth_header = {'Authorization': {
        'description': 'Bearer <JWT Token>',
        'in': 'header',
        'type': 'string',
        'required': True
    }
}


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        facade = current_app.extensions['FACADE']
        amenity_data = api.payload

        if not amenity_data.get('name'):
            return {'error': 'Amenity name is required'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        facade = current_app.extensions['FACADE']
        amenities = facade.get_all_amenities()
        amenity_list = []
        for amenity in amenities:
            amenity_list.append({
                'id': amenity.id,
                'name': amenity.name
            })
        return amenity_list, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        facade = current_app.extensions['FACADE']
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        facade = current_app.extensions['FACADE']
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        amenity_data = api.payload
        if not amenity_data.get('name'):
            return {'error': 'Amenity name is required'}, 400

        facade.update_amenity(amenity_id, amenity_data)
        updated_amenity = facade.get_amenity(amenity_id)
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200
    
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity"""
        facade = current_app.extensions['FACADE']
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        facade.delete_amenity(amenity_id)
        return {'message': f'Place {amenity_id} deleted successfully'}, 200