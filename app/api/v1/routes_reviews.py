from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity # type: ignore


api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

auth_header = {'Authorization': {
        'description': 'Bearer <JWT Token>',
        'in': 'header',
        'type': 'string',
        'required': True
    }
}

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def post(self):
        """Register a new review"""
        facade = current_app.extensions['FACADE']
        current_user = get_jwt_identity()
        review_data = api.payload

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400

        if review_data["user_id"] != current_user["id"]:
            return {'error': 'Unauthorized action'}, 403

        if place.owner_id == current_user["id"]:
            return {'error': 'Unauthorized action: You cannot review your own place.'}, 403

        reviews = facade.get_all_reviews()
        for review in reviews:
            if current_user["id"] == review.user_id and place.id == review.place_id:
                return {'error': 'Unauthorized action: You already reviewed this place.'}, 403


        if not all(key in review_data for key in ('user_id', 'place_id', 'rating', 'text')):
            return {'error': 'Missing required fields'}, 400

 
        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 400

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400

        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        facade = current_app.extensions['FACADE']
        reviews = facade.get_all_reviews()
        review_list = []
        for review in reviews:
            review_list.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            })
        return review_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        facade = current_app.extensions['FACADE']
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        facade = current_app.extensions['FACADE']

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        if not is_admin and review.user_id != current_user["id"]:
            return {'error': 'Unauthorized action, you can only update your own reviews'}, 403

        review_data = api.payload

        if not is_admin and review_data["user_id"] != current_user["id"]:
            return {'error': 'Unauthorized action, a review must contain your id'}, 403

        try:
            facade.update_review(review_id, review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        updated_review = facade.get_review(review_id)
        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user_id': updated_review.user_id,
            'place_id': updated_review.place_id
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.doc('update_user', params=auth_header)
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        facade = current_app.extensions['FACADE']

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        if not is_admin and review.user_id != current_user["id"]:
            return {'error': 'Unauthorized action, you can only delete your own reviews'}, 403

        facade.delete_review(review_id)
        return {'message': f'Review {review_id} deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        facade = current_app.extensions['FACADE']
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        reviews_list = []
        for review in reviews:
            reviews_list.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            })
        return reviews_list, 200