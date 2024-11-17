import unittest
from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class TestPlaceModel(unittest.TestCase):
    def test_place_creation(self):
        """Test creation of a Place instance"""
        place = Place(
            title="Beach House",
            description="A lovely beach house with ocean views.",
            price=200.0,
            latitude=36.7783,
            longitude=-119.4179,
            owner="John Doe",
            owner_id="123e4567-e89b-12d3-a456-426614174000",
            reviews=[{"text": "Great place!", "rating": 5}],
            amenities=["Wi-Fi", "Pool"],
        )

        # Assert all attributes
        self.assertEqual(place.title, "Beach House")
        self.assertEqual(place.description, "A lovely beach house with ocean views.")
        self.assertEqual(place.price, 200.0)
        self.assertEqual(place.latitude, 36.7783)
        self.assertEqual(place.longitude, -119.4179)
        self.assertEqual(place.owner, "John Doe")
        self.assertEqual(place.owner_id, "123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(place.reviews, [{"text": "Great place!", "rating": 5}])
        self.assertEqual(place.amenities, ["Wi-Fi", "Pool"])

    def test_place_relationships(self):
        """Test relationships of Place with User, Review, and Amenity models"""
        # Mock related objects
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        review = Review(text="Amazing stay!", rating=5)
        amenity = Amenity(name="Wi-Fi")

        # Create Place instance and assign relationships
        place = Place(title="Beach House", description="Lovely house", price=200.0, latitude=36.0, longitude=-119.0)
        place.place_owner = user
        place.review_ids.append(review)
        place.amenities_obj.append(amenity)

        # Assert relationships
        self.assertEqual(place.place_owner.first_name, "John")
        self.assertEqual(len(place.review_ids), 1)
        self.assertEqual(place.review_ids[0].text, "Amazing stay!")
        self.assertEqual(len(place.amenities_obj), 1)
        self.assertEqual(place.amenities_obj[0].name, "Wi-Fi")


if __name__ == "__main__":
    unittest.main()