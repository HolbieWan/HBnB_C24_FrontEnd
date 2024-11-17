import unittest
from app import create_app

class TestAuthEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test client and shared test data"""
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        # Create a user for login tests
        cls.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "testpassword"
        }

        facade = cls.app.extensions['FACADE']
        try:
            cls.test_user = facade.create_user(cls.user_data)
        except ValueError:
            cls.test_user = facade.get_user_by_email(cls.user_data['email'])

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        facade = cls.app.extensions['FACADE']
        facade.delete_user(cls.test_user.id)
        cls.app_context.pop()

    def test_valid_login(self):
        """Test login endpoint with valid credentials"""
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/v1/login/', json=login_data)
        self.assertEqual(response.status_code, 200)
        token = response.get_json().get('access_token')
        self.assertIsNotNone(token)
        self.assertIn('access_token', response.get_json())

    def test_invalid_login(self):
        """Test login endpoint with invalid credentials"""
        login_data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/v1/login/', json=login_data)
        self.assertEqual(response.status_code, 401)
        error = response.get_json().get('error')
        self.assertEqual(error, 'Invalid credentials')

    def test_nonexistent_user_login(self):
        """Test login endpoint with a nonexistent user"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/v1/login/', json=login_data)
        self.assertEqual(response.status_code, 401)
        error = response.get_json().get('error')
        self.assertEqual(error, 'Invalid credentials')

    def test_login_missing_email(self):
        """Test login endpoint with missing email"""
        login_data = {
            'password': self.user_data['password']
        }
        response = self.client.post('/api/v1/login/', json=login_data)
        self.assertEqual(response.status_code, 400)
        error = response.get_json().get('error')
        self.assertEqual(error, 'Missing email')

    def test_login_missing_password(self):
        """Test login endpoint with missing password"""
        login_data = {
            'email': self.user_data['email']
        }
        response = self.client.post('/api/v1/login/', json=login_data)
        self.assertEqual(response.status_code, 400)
        error = response.get_json().get('error')
        self.assertEqual(error, 'Missing password')

    def test_empty_payload(self):
        """Test login endpoint with empty payload"""
        response = self.client.post('/api/v1/login/', json={})
        self.assertEqual(response.status_code, 400)
        error = response.get_json().get('error')
        self.assertEqual(error, 'Missing email')


if __name__ == '__main__':
    unittest.main()