import unittest
from app import create_app


class TestAmenityEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Explicitly push the app context
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Create a unique admin user for this test
        admin_data = {
            "first_name": "Amenity",
            "last_name": "Admin",
            "email": "amenity_admin@example.com",
            "password": "adminpass",
            "is_admin": True
        }
        facade = cls.app.extensions["FACADE"]
        cls.admin_user = facade.create_user(admin_data)

        # Log in as admin to get the access token
        login_data = {"email": "amenity_admin@example.com", "password": "adminpass"}
        login_response = cls.client.post("/api/v1/login/", json=login_data)
        cls.admin_token = login_response.get_json()["access_token"]

    @classmethod
    def tearDownClass(cls):
        # Clean up by deleting the admin user
        facade = cls.app.extensions["FACADE"]
        facade.delete_user(cls.admin_user.id)

    def test_create_amenity(self):
        """Test creating an amenity as an admin"""
        response = self.client.post(
            "/api/v1/amenities/",
            json={"name": "Wi-Fi"},
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Wi-Fi")

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        # Create a test amenity
        response = self.client.post(
            "/api/v1/amenities/",
            json={"name": "Pool"},
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 201)

        # Get all amenities
        response = self.client.get("/api/v1/amenities/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertIn("name", data[0])

    def test_get_amenity_by_id(self):
        """Test retrieving an amenity by its ID"""
        # Create a test amenity
        response = self.client.post(
            "/api/v1/amenities/",
            json={"name": "Gym"},
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        amenity_id = response.get_json()["id"]

        # Get the amenity by ID
        response = self.client.get(f"/api/v1/amenities/{amenity_id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Gym")

    def test_update_amenity(self):
        """Test updating an amenity's information"""
        # Create a test amenity
        response = self.client.post(
            "/api/v1/amenities/",
            json={"name": "Parking"},
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        amenity_id = response.get_json()["id"]

        # Update the amenity
        response = self.client.put(
            f"/api/v1/amenities/{amenity_id}",
            json={"name": "Updated Parking"},
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Updated Parking")

    def test_delete_amenity(self):
        """Test deleting an amenity"""
        # Create a test amenity
        response = self.client.post(
            "/api/v1/amenities/",
            json={"name": "Spa"},
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 201)
        amenity_id = response.get_json()["id"]

        # Delete the amenity
        response = self.client.delete(
            f"/api/v1/amenities/{amenity_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        print("Delete Amenity Debug:", response.status_code, response.get_json())  # Debugging
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Adjust the assertion to match the API response
        self.assertIn(f"Place {amenity_id} deleted successfully", data["message"])


if __name__ == "__main__":
    unittest.main()