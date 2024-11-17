import unittest
from app import create_app
import uuid

class TestUserEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Create a unique admin user for this test class
        admin_email = f"admin_user_{uuid.uuid4()}@example.com"
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": admin_email,
            "password": "adminpass",
            "is_admin": True,
        }
        facade = cls.app.extensions['FACADE']
        cls.admin_user = facade.create_user(admin_data)

        # Log in as admin to get the access token
        login_data = {"email": admin_email, "password": "adminpass"}
        login_response = cls.client.post('/api/v1/login/', json=login_data)
        cls.admin_token = login_response.get_json().get("access_token")

        # Create a regular user for non-admin tests
        user_email = f"user_{uuid.uuid4()}@example.com"
        user_data = {
            "first_name": "Regular",
            "last_name": "User",
            "email": user_email,
            "password": "userpass",
        }
        cls.regular_user = facade.create_user(user_data)

        # Log in as regular user
        login_data = {"email": user_email, "password": "userpass"}
        login_response = cls.client.post('/api/v1/login/', json=login_data)
        cls.user_token = login_response.get_json().get("access_token")

    @classmethod
    def tearDownClass(cls):
        facade = cls.app.extensions['FACADE']
        facade.delete_user(cls.admin_user.id)
        facade.delete_user(cls.regular_user.id)
        cls.app_context.pop()

    def test_unauthorized_access(self):
        """Test unauthorized access for creating a user"""
        headers = {"Authorization": f"Bearer {self.user_token}"}
        user_data = {
            "first_name": "Unauthorized",
            "last_name": "User",
            "email": f"unauth_{uuid.uuid4()}@example.com",
            "password": "password123",
        }
        response = self.client.post('/api/v1/users/', json=user_data, headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json().get("error"), "Admin privileges required")

    def test_duplicate_email(self):
        """Test creating a user with a duplicate email"""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        user_data = {
            "first_name": "Duplicate",
            "last_name": "User",
            "email": self.regular_user.email,  # Using an existing email
            "password": "password123",
        }
        response = self.client.post('/api/v1/users/', json=user_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json().get("error"), "Email already registered")

    def test_get_nonexistent_user(self):
        """Test retrieving a nonexistent user"""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        nonexistent_user_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/users/{nonexistent_user_id}', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json().get("error"), "User not found")

    def test_update_own_data(self):
        """Test a non-admin user updating their own data"""
        headers = {"Authorization": f"Bearer {self.user_token}"}
        user_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": self.regular_user.email,  # Keep email the same
            "password": "newpassword",
        }
        response = self.client.put(f'/api/v1/users/{self.regular_user.id}', json=user_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertEqual(response_json["first_name"], "Updated")
        self.assertEqual(response_json["last_name"], "User")

    def test_update_other_user_as_regular_user(self):
        """Test a regular user trying to update another user's data"""
        headers = {"Authorization": f"Bearer {self.user_token}"}
        user_data = {
            "first_name": "Hack",
            "last_name": "Attempt",
            "email": self.admin_user.email,
            "password": "hackpass",
        }
        response = self.client.put(f'/api/v1/users/{self.admin_user.id}', json=user_data, headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json().get("error"), "Unauthorized action, you can only modify your own data")

    def test_delete_nonexistent_user(self):
        """Test deleting a nonexistent user"""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        nonexistent_user_id = str(uuid.uuid4())
        response = self.client.delete(f'/api/v1/users/{nonexistent_user_id}', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json().get("error"), "User not found")

    def test_delete_other_user_as_regular_user(self):
        """Test a regular user trying to delete another user's data"""
        headers = {"Authorization": f"Bearer {self.user_token}"}
        response = self.client.delete(f'/api/v1/users/{self.admin_user.id}', headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json().get("error"), "Unauthorized action, you can only modify your own data")


if __name__ == "__main__":
    unittest.main()