import unittest
from flask import Flask
from app.extensions import db
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class TestSQLAlchemyRepository(unittest.TestCase):
    def setUp(self):
        """Set up the test app, database, and repository"""
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory SQLite database
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Initialize database
        db.init_app(self.app)

        # Set up app context
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()  # Create all database tables

        # Initialize repository
        self.repo = SQLAlchemyRepository(User)

        # Create mock users
        self.user1 = User(
            id="1",
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            password="password123"
        )
        self.user2 = User(
            id="2",
            first_name="Bob",
            last_name="Smith",
            email="bob@example.com",
            password="password456"
        )

        # Add mock users to the database
        self.repo.add(self.user1)
        self.repo.add(self.user2)

    def tearDown(self):
        """Tear down the test database"""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_add_and_get(self):
        """Test adding and retrieving an object"""
        retrieved_user = self.repo.get(self.user1.id)

        # Assertions
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.first_name, "Alice")
        self.assertEqual(retrieved_user.email, "alice@example.com")

    def test_get_all(self):
        """Test retrieving all objects"""
        all_users = self.repo.get_all()

        # Assertions
        self.assertEqual(len(all_users), 2)
        self.assertTrue(any(user.first_name == "Alice" for user in all_users))
        self.assertTrue(any(user.first_name == "Bob" for user in all_users))

    def test_update(self):
        """Test updating an object"""
        self.repo.update(self.user1.id, {"first_name": "Alicia"})
        updated_user = self.repo.get(self.user1.id)

        # Assertions
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, "Alicia")

    def test_delete(self):
        """Test deleting an object"""
        self.repo.delete(self.user1.id)
        deleted_user = self.repo.get(self.user1.id)

        # Assertions
        self.assertIsNone(deleted_user)

    def test_get_by_attribute(self):
        """Test retrieving an object by an attribute"""
        retrieved_user = self.repo.get_by_attribute("email", "bob@example.com")

        # Assertions
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.first_name, "Bob")


if __name__ == "__main__":
    unittest.main()