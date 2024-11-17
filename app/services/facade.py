# facade.py

from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # User methods
    def create_user(self, user_data):
        if not isinstance(user_data.get('first_name'), str) or not (1 <= len(user_data.get('first_name', '')) <= 50):
            raise ValueError('First_name must be a string between 1 and 50 characters')
        if not isinstance(user_data.get('last_name'), str) or not (1 <= len(user_data.get('last_name', '')) <= 50):
            raise ValueError('Last_name must be a string between 1 and 50 characters')
        
        user = User(**user_data)
        user.hash_password(user_data["password"])

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        updated_user = self.get_user(user_id)
        return updated_user
    
    def delete_user(self, user_id):
        print(f"Deleting User: {user_id} ")
        self.user_repo.delete(user_id)

    # Amenity methods
    def create_amenity(self, amenity_data):
        if not isinstance(amenity_data.get('name'), str) or not (1 <= len(amenity_data.get("name", "")) <= 50):
            raise ValueError('Name must be between 1 and 50 characters')
        
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        print(f"Deliting Amenity: {amenity_id} ")
        self.amenity_repo.delete(amenity_id)


    # Place methods
    def create_place(self, place_data):
        if not isinstance(place_data.get('price'), (int, float)) or not (1 <= place_data.get("price") <= 1000000):
            raise ValueError('Price must be a number')
        if not isinstance(place_data.get('latitude'), (int, float)) or not (-90 <= place_data.get("latitude") <= 90):
            raise ValueError('Latitude must be a number')
        if not isinstance(place_data.get('longitude'), (int, float)) or not (-180 <= place_data.get("longitude") <= 180):
            raise ValueError('Longitude must be a number')
        if not isinstance(place_data.get('title'), str) or not (1 <= len(place_data.get("title", "")) <= 50):
            raise ValueError('Title must be between 1 and 50 characters')
        if not isinstance(place_data.get('description'), str) or not (1 <= len(place_data.get("description", "")) <= 500):
            raise ValueError('Description must be between 1 and 500 characters')

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        updated_place = self.get_place(place_id)
        return updated_place

    def delete_place(self, place_id):
        print(f"Deleting Place: {place_id}")
        self.place_repo.delete(place_id)

    # Review methods
    def create_review(self, review_data):
        if not self.get_user(review_data.get('user_id')):
            raise ValueError('User does not exist')
        if not self.get_place(review_data.get('place_id')):
            raise ValueError('Place does not exist')
        if not isinstance(review_data.get('rating'), int) or not (1 <= review_data['rating'] <= 5):
            raise ValueError('Rating must be an integer between 1 and 5')
        if not isinstance(review_data.get('text'), str) or not (1 <= len(review_data.get("text", "")) <= 500):
            raise ValueError('Text must be between 1 and 500 characters')

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        print(f"Deleting Review: {review_id}")
        self.review_repo.delete(review_id)