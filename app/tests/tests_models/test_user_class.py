import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        """Test creation of a User instance"""
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", is_admin=True)

        # Assert User attributes
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertTrue(user.is_admin)

    def test_user_password_hashing(self):
        """Test password hashing and verification"""
        user = User(first_name="Jane", last_name="Smith", email="jane.smith@example.com")
        user.hash_password("securepassword")

        # Assert password hashing and verification
        self.assertTrue(user.verify_password("securepassword"))
        self.assertFalse(user.verify_password("wrongpassword"))

    def test_user_relationships(self):
        """Test relationships of User with Place and Review models"""
        # Mock related objects
        place = Place(title="Cozy Cabin", description="A warm cabin in the woods.", price=150.0, latitude=40.0, longitude=-120.0)
        review = Review(text="Had a great time!", rating=5)

        # Create User instance and assign relationships
        user = User(first_name="Alice", last_name="Smith", email="alice@example.com")
        user.places.append(place)
        user.reviews.append(review)

        # Assert relationships
        self.assertEqual(len(user.places), 1)
        self.assertEqual(user.places[0].title, "Cozy Cabin")
        self.assertEqual(len(user.reviews), 1)
        self.assertEqual(user.reviews[0].text, "Had a great time!")


if __name__ == "__main__":
    unittest.main()