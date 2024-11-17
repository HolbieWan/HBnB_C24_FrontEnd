from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity # type: ignore


api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    # 'owner' is not included in the input payload; it's added in the response
    'amenities': fields.List(fields.String, required=True, description="List of amenity IDs")
})

auth_header = {'Authorization': {
        'description': 'Bearer <JWT Token>',
        'in': 'header',
        'type': 'string',
        'required': True
    }
}


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        facade = current_app.extensions['FACADE']

        place_data = api.payload

        if place_data["owner_id"] != current_user["id"]:
            return {'error': 'Unauthorized action, can only create place if you are the owner'}, 403

        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id', 'amenities']
        if not all(field in place_data and place_data[field] for field in required_fields):
            return {'error': 'Missing required fields'}, 400

        owner = facade.get_user(place_data.get('owner_id'))
        if not owner:
            return {'error': 'Owner not found'}, 400

        amenity_ids = place_data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': f'Amenity with ID {amenity_id} not found'}, 400

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        new_place.amenities = amenity_ids

        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id,
            'amenities': new_place.amenities
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        facade = current_app.extensions['FACADE']
        places = facade.get_all_places()
        place_list = []
        for place in places:
            owner = facade.get_user(place.owner_id)
            owner_data = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            } if owner else None
            place_list.append({
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id,
                'owner': owner_data,
                'amenities': place.amenities
            })
        return place_list, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        facade = current_app.extensions['FACADE']
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        owner = facade.get_user(place.owner_id)
        owner_data = {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'email': owner.email
        } if owner else None

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'owner': owner_data,
            'amenities': place.amenities 
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        facade = current_app.extensions['FACADE']

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        if not is_admin and place.owner_id != current_user["id"]:
            return {'error': 'Unauthorized action, you must be the owner of the place to update it'}, 403

        place_data = api.payload

        if 'amenities' in place_data:
            amenity_ids = place_data['amenities']
            for amenity_id in amenity_ids:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {'error': f'Amenity with ID {amenity_id} not found'}, 400

            place.amenities = amenity_ids

        updated_place = facade.update_place(place_id, place_data)
        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner_id': updated_place.owner_id,
            'amenities': updated_place.amenities
        }, 200
    
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)

        facade = current_app.extensions['FACADE']
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        if not is_admin and place.owner_id != current_user["id"]:
            return {'error': 'Unauthorized action, you must be the owner of the place to delete it'}, 403

        facade.delete_place(place_id)
        return {'message': f'Place {place_id} deleted successfully'}, 200