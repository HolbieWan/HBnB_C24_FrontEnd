import unittest
from app.models.review import Review
from app.models.place import Place
from app.models.user import User


class TestReviewModel(unittest.TestCase):
    def test_review_creation(self):
        """Test creation of a Review instance"""
        review = Review(
            text="Amazing place, had a wonderful time!",
            rating=5,
            place_id="123e4567-e89b-12d3-a456-426614174001",
            user_id="123e4567-e89b-12d3-a456-426614174000"
        )

        # Assert attributes
        self.assertEqual(review.text, "Amazing place, had a wonderful time!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place_id, "123e4567-e89b-12d3-a456-426614174001")
        self.assertEqual(review.user_id, "123e4567-e89b-12d3-a456-426614174000")

    def test_review_relationships(self):
        """Test relationships between Review, Place, and User models"""
        # Create mock Place and User instances
        place = Place(
            title="Mountain Cabin",
            description="A beautiful cabin in the mountains.",
            price=300.0,
            latitude=35.0,
            longitude=-120.0,
            owner_id="123e4567-e89b-12d3-a456-426614174000"
        )
        user = User(first_name="Alice", last_name="Smith", email="alice@example.com")

        # Create a Review instance and set relationships
        review = Review(text="Best vacation ever!", rating=5)
        review.place = place
        review.user = user

        # Assert relationships
        self.assertEqual(review.place.title, "Mountain Cabin")
        self.assertEqual(review.user.first_name, "Alice")
        self.assertEqual(review.user.email, "alice@example.com")

if __name__ == "__main__":
    unittest.main()