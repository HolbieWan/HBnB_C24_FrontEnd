import unittest
from app.models.amenity import Amenity
from app.models.place import Place


class TestAmenityModel(unittest.TestCase):
    def test_amenity_creation(self):
        """Test creation of an Amenity instance"""
        amenity = Amenity(name="Wi-Fi")

        # Assert attributes
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_amenity_relationships(self):
        """Test relationships of Amenity with Place model"""
        # Create mock Place instance
        place = Place(
            title="Luxury Villa",
            description="A luxurious villa with a pool.",
            price=500.0,
            latitude=34.0522,
            longitude=-118.2437,
            owner_id="123e4567-e89b-12d3-a456-426614174000"
        )

        # Create Amenity instance
        amenity = Amenity(name="Swimming Pool")
        amenity.places.append(place)

        # Assert relationships
        self.assertEqual(len(amenity.places), 1)
        self.assertEqual(amenity.places[0].title, "Luxury Villa")


if __name__ == "__main__":
    unittest.main()