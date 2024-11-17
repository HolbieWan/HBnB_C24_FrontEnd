import unittest
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Explicitly push the app context
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        facade = cls.app.extensions['FACADE']

        # Check if the admin user already exists
        admin_user = facade.get_user_by_email("admin@example.com")
        if not admin_user:
            admin_data = {
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@example.com",
                "password": "adminpass",
                "is_admin": True
            }
            admin_user = facade.create_user(admin_data)

        cls.admin_user = admin_user

        # Log in as admin to get the access token
        login_data = {
            "email": "admin@example.com",
            "password": "adminpass"
        }
        login_response = cls.client.post('/api/v1/login/', json=login_data)
        login_response_json = login_response.get_json()
        if login_response.status_code != 200 or not login_response_json:
            raise RuntimeError("Failed to log in as admin")
        cls.admin_token = login_response_json.get("access_token")

        # Create amenities for tests
        cls.amenity1 = facade.create_amenity({"name": "Pool"})
        cls.amenity2 = facade.create_amenity({"name": "Wi-Fi"})

    @classmethod
    def tearDownClass(cls):
        facade = cls.app.extensions['FACADE']

        # Clean up amenities
        facade.delete_amenity(cls.amenity1.id)
        facade.delete_amenity(cls.amenity2.id)

        # Clean up admin user
        facade.delete_user(cls.admin_user.id)

        # Pop the app context
        cls.app_context.pop()

    def test_create_place(self):
        """Test creating a new place successfully"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful Apartment",
            "description": "A cozy apartment in the city center",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.admin_user.id,
            "amenities": [self.amenity1.id, self.amenity2.id]
        }, headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('title', data)
        self.assertEqual(data['title'], 'Beautiful Apartment')

    def test_get_all_places(self):
        """Test retrieving all places"""
        response = self.client.get('/api/v1/places/', headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)

    def test_get_place_by_id(self):
        """Test retrieving a place by its ID"""
        # First create a place
        response = self.client.post('/api/v1/places/', json={
            "title": "Luxury Villa",
            "description": "A luxurious villa with a pool",
            "price": 500.0,
            "latitude": 45.4215,
            "longitude": -75.6903,
            "owner_id": self.admin_user.id,
            "amenities": [self.amenity1.id]
        }, headers={"Authorization": f"Bearer {self.admin_token}"})
        place_id = response.get_json()['id']

        # Now get the place by ID
        response = self.client.get(f'/api/v1/places/{place_id}', headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Luxury Villa')

    def test_update_place(self):
        """Test updating a place's information"""
        # First create a place to update
        response = self.client.post('/api/v1/places/', json={
            "title": "Small Cottage",
            "description": "A small, cozy cottage",
            "price": 50.0,
            "latitude": 52.5200,
            "longitude": 13.4050,
            "owner_id": self.admin_user.id,
            "amenities": [self.amenity1.id]
        }, headers={"Authorization": f"Bearer {self.admin_token}"})
        place_id = response.get_json()['id']

        # Now update the place
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Cottage",
            "description": "An updated cozy cottage",
            "price": 60.0,
            "amenities": [self.amenity2.id]
        }, headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated Cottage')
        self.assertEqual(data['price'], 60.0)

    def test_delete_place(self):
        """Test deleting a place by ID"""
        # First create a place to delete
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "A lovely beach house",
            "price": 200.0,
            "latitude": 36.7783,
            "longitude": -119.4179,
            "owner_id": self.admin_user.id,
            "amenities": [self.amenity1.id]
        }, headers={"Authorization": f"Bearer {self.admin_token}"})
        place_id = response.get_json()['id']

        # Now delete the place
        response = self.client.delete(f'/api/v1/places/{place_id}', headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Place {place_id} deleted successfully', response.get_json()['message'])

    def test_get_place_by_id_not_found(self):
        """Test retrieving a place with a non-existent ID"""
        response = self.client.get('/api/v1/places/nonexistent-id', headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['error'])

    def test_update_place_not_found(self):
        """Test updating a place with a non-existent ID"""
        response = self.client.put('/api/v1/places/nonexistent-id', json={
            "title": "Nonexistent Place",
            "price": 99.0
        }, headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['error'])

    def test_delete_place_not_found(self):
        """Test deleting a place with a non-existent ID"""
        response = self.client.delete('/api/v1/places/nonexistent-id', headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['error'])


if __name__ == "__main__":
    unittest.main()