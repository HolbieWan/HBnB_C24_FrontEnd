import unittest
import uuid
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        facade = cls.app.extensions["FACADE"]

        # Create a unique admin user for this test class
        admin_email = f"admin_review_{uuid.uuid4()}@example.com"
        admin_data = {
            "first_name": "Admin",
            "last_name": "Reviewer",
            "email": admin_email,
            "password": "adminpass",
            "is_admin": True,
        }
        cls.admin_user = facade.create_user(admin_data)

        # Log in as admin
        login_response = cls.client.post(
            "/api/v1/login/",
            json={"email": admin_email, "password": "adminpass"},
        )
        cls.admin_token = login_response.get_json()["access_token"]

        # Create two regular users
        cls.user1_data = {
            "first_name": "User1",
            "last_name": "One",
            "email": f"user1_{uuid.uuid4()}@example.com",
            "password": "user1pass",
        }
        cls.user2_data = {
            "first_name": "User2",
            "last_name": "Two",
            "email": f"user2_{uuid.uuid4()}@example.com",
            "password": "user2pass",
        }
        cls.user1 = facade.create_user(cls.user1_data)
        cls.user2 = facade.create_user(cls.user2_data)

        # Log in as user2
        login_response = cls.client.post(
            "/api/v1/login/",
            json={"email": cls.user2_data["email"], "password": "user2pass"},
        )
        cls.user2_token = login_response.get_json()["access_token"]

    @classmethod
    def tearDownClass(cls):
        facade = cls.app.extensions["FACADE"]

        # Delete users
        facade.delete_user(cls.user1.id)
        facade.delete_user(cls.user2.id)
        facade.delete_user(cls.admin_user.id)
        cls.app_context.pop()

    def create_place(self, owner_id):
        """Helper method to create a place."""
        facade = self.app.extensions["FACADE"]
        return facade.create_place({
            "title": "Test Place",
            "description": "Testing place",
            "price": 200.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id,
        })

    def test_create_review(self):
        """Test creating a review successfully"""
        place = self.create_place(self.user1.id)
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Amazing place!",
                "rating": 5,
                "user_id": self.user2.id,
                "place_id": place.id,
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["text"], "Amazing place!")
        self.assertEqual(data["rating"], 5)

    def test_create_review_invalid_place(self):
        """Test creating a review with an invalid place_id"""
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place!",
                "rating": 5,
                "user_id": self.user2.id,
                "place_id": "nonexistent-place-id",
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Place not found", response.get_json()["error"])

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        place = self.create_place(self.user1.id)

        # Create a review
        self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Good place!",
                "rating": 4,
                "user_id": self.user2.id,
                "place_id": place.id,
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )

        # Get all reviews
        response = self.client.get("/api/v1/reviews/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)

    def test_get_review_by_id(self):
        """Test retrieving a review by ID"""
        place = self.create_place(self.user1.id)

        # Create a review
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Nice location!",
                "rating": 5,
                "user_id": self.user2.id,
                "place_id": place.id,
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        review_id = response.get_json()["id"]

        # Retrieve the review
        response = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], review_id)
        self.assertEqual(data["text"], "Nice location!")

    def test_update_review(self):
        """Test updating a review"""
        place = self.create_place(self.user1.id)

        # Create a review
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Decent place.",
                "rating": 3,
                "user_id": self.user2.id,
                "place_id": place.id,
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        review_id = response.get_json()["id"]

        # Update the review
        response = self.client.put(
            f"/api/v1/reviews/{review_id}",
            json={
                "text": "Updated review text.",
                "rating": 4,
                "user_id": self.user2.id,
                "place_id": place.id,
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["text"], "Updated review text.")
        self.assertEqual(data["rating"], 4)

    def test_delete_review(self):
        """Test deleting a review"""
        place = self.create_place(self.user1.id)

        # Create a review
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Temporary review.",
                "rating": 2,
                "user_id": self.user2.id,
                "place_id": place.id,
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        review_id = response.get_json()["id"]

        # Delete the review
        response = self.client.delete(
            f"/api/v1/reviews/{review_id}",
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        self.assertEqual(response.status_code, 200)

        # Confirm deletion
        response = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_for_place(self):
        """Test retrieving all reviews for a specific place"""
        # Create a place owned by user1
        place = self.create_place(self.user1.id)
        print(f"[DEBUG] Created Place: {place.id}")

        # Create a review for the place by user2
        review1_response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Rastaman vibration yeahhh",
                "rating": 5,
                "user_id": self.user2.id,
                "place_id": place.id,
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        print(f"[DEBUG] Review 1 Response: {review1_response.status_code}, {review1_response.get_json()}")
        self.assertEqual(review1_response.status_code, 201)

        # Get all reviews for the place
        response = self.client.get(
            f"/api/v1/reviews/places/{place.id}/reviews",
            headers={"Authorization": f"Bearer {self.user2_token}"},  # Ensure token is provided
        )
        print(f"[DEBUG] Get Reviews Response: {response.status_code}, {response.get_json()}")

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Verify the content of the response
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        # Check the review details
        review = data[0]
        self.assertEqual(review["place_id"], place.id)
        self.assertEqual(review["text"], "Rastaman vibration yeahhh")
        self.assertEqual(review["rating"], 5)
        self.assertEqual(review["user_id"], self.user2.id)


if __name__ == "__main__":
    unittest.main()