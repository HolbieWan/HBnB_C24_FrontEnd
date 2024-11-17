import unittest
from app.services.facade import HBnBFacade
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from flask import Flask
import uuid


class TestHBnBFacade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the testing environment and initialize the app."""
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(cls.app)
        cls.facade = HBnBFacade()

        with cls.app.app_context():
            db.create_all()

        # Test data
        cls.user_data = {
            "first_name": "Alice",
            "last_name": "Doe",
            "email": "alice@example.com",
            "password": "password123"
        }
        cls.place_data = {
            "title": "Cozy Cottage",
            "description": "A cozy cottage in the countryside",
            "price": 150.0,
            "latitude": 45.0,
            "longitude": -93.0,
            "owner_id": None  # Will be set dynamically
        }
        cls.amenity_data = {
            "name": "WiFi"
        }
        cls.review_data = {
            "text": "Amazing place!",
            "rating": 5,
            "place_id": None,  # Will be set dynamically
            "user_id": None   # Will be set dynamically
        }

    def test_facade_operations(self):
        """Test facade operations in sequence"""

        with self.app.app_context():
            # Create user
            print("Creating user...")
            user = self.facade.create_user(self.user_data)
            db.session.commit()
            print(f"Created user: {user}")
            self.assertIsNotNone(user)
            self.assertEqual(user.first_name, "Alice")

            # Get user
            user_id = str(user.id)  # Ensure it's a string UUID
            retrieved_user = self.facade.get_user(user_id)
            print(f"Retrieved user: {retrieved_user}")
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.email, "alice@example.com")

            # Create place
            print("Creating place...")
            self.place_data["owner_id"] = user_id  # Set the owner_id to match the created user
            place = self.facade.create_place(self.place_data)
            db.session.commit()
            print(f"Created place: {place}")
            self.assertIsNotNone(place)
            self.assertEqual(place.title, "Cozy Cottage")

            # Get place
            place_id = str(place.id)  # Ensure it's a string UUID
            retrieved_place = self.facade.get_place(place_id)
            print(f"Retrieved place: {retrieved_place}")
            self.assertIsNotNone(retrieved_place)
            self.assertEqual(retrieved_place.title, "Cozy Cottage")

            # Create amenity
            print("Creating amenity...")
            amenity = self.facade.create_amenity(self.amenity_data)
            db.session.commit()
            print(f"Created amenity: {amenity}")
            self.assertIsNotNone(amenity)
            self.assertEqual(amenity.name, "WiFi")

            # Get amenity
            amenity_id = str(amenity.id)  # Ensure it's a string UUID
            retrieved_amenity = self.facade.get_amenity(amenity_id)
            print(f"Retrieved amenity: {retrieved_amenity}")
            self.assertIsNotNone(retrieved_amenity)
            self.assertEqual(retrieved_amenity.name, "WiFi")

            # Create review
            print("Creating review...")
            self.review_data["place_id"] = place_id
            self.review_data["user_id"] = user_id
            review = self.facade.create_review(self.review_data)
            db.session.commit()
            print(f"Created review: {review}")
            self.assertIsNotNone(review)
            self.assertEqual(review.text, "Amazing place!")

            # Get review
            review_id = str(review.id)  # Ensure it's a string UUID
            retrieved_review = self.facade.get_review(review_id)
            print(f"Retrieved review: {retrieved_review}")
            self.assertIsNotNone(retrieved_review)
            self.assertEqual(retrieved_review.rating, 5)

            # Delete amenity
            print("Deleting amenity...")
            self.facade.delete_amenity(amenity_id)
            db.session.commit()
            deleted_amenity = self.facade.get_amenity(amenity_id)
            self.assertIsNone(deleted_amenity)

            # Delete review
            print("Deleting review...")
            self.facade.delete_review(review_id)
            db.session.commit()
            deleted_review = self.facade.get_review(review_id)
            self.assertIsNone(deleted_review)

            # Delete place
            print("Deleting place...")
            self.facade.delete_place(place_id)
            db.session.commit()
            deleted_place = self.facade.get_place(place_id)
            self.assertIsNone(deleted_place)

            # Delete user
            print("Deleting user...")
            self.facade.delete_user(user_id)
            db.session.commit()
            deleted_user = self.facade.get_user(user_id)
            self.assertIsNone(deleted_user)


if __name__ == "__main__":
    unittest.main()