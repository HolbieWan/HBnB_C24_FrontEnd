import unittest
from app.models.user import User
from app.persistence.repository import InMemoryRepository


class TestInMemoryRepository(unittest.TestCase):
    def setUp(self):
        """Set up the repository and mock data"""
        self.repo = InMemoryRepository()

        # Ensure user objects have IDs and all necessary attributes
        self.user1 = User(id="1", first_name="Alice", last_name="Doe", email="alice@example.com")
        self.user2 = User(id="2", first_name="Bob", last_name="Smith", email="bob@example.com")

    def test_add_and_get(self):
        """Test adding and retrieving an object"""
        self.repo.add(self.user1)  # Add a user to the repository

        # Debugging: Check the repository storage
        print(f"Repository Storage: {self.repo._storage}")

        retrieved_user = self.repo.get(self.user1.id)  # Retrieve the user by ID

        # Debugging: Check the retrieved user
        print(f"Retrieved User: {retrieved_user}")

        # Assertions
        self.assertIsNotNone(retrieved_user)  # Ensure the user is not None
        self.assertEqual(retrieved_user.first_name, "Alice") # type: ignore
        self.assertEqual(retrieved_user.email, "alice@example.com") # type: ignore

    def test_get_all(self):
        """Test retrieving all objects"""
        self.repo.add(self.user1)
        self.repo.add(self.user2)

        # Retrieve all users
        all_users = self.repo.get_all()

        # Debugging: Check all users
        print(f"All Users: {all_users}")

        # Assertions
        self.assertEqual(len(all_users), 2)
        self.assertIn(self.user1, all_users)
        self.assertIn(self.user2, all_users)

    def test_update(self):
        """Test updating an object"""
        self.repo.add(self.user1)  # Add a user to the repository
        self.repo.update(self.user1.id, {"first_name": "Alicia"})  # Update the user's first name

        updated_user = self.repo.get(self.user1.id)  # Retrieve the updated user

        # Debugging: Check the updated user
        print(f"Updated User: {updated_user}")

        # Assertions
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, "Alicia") # type: ignore

    def test_delete(self):
        """Test deleting an object"""
        self.repo.add(self.user1)  # Add a user to the repository
        self.repo.delete(self.user1.id)  # Delete the user by ID

        deleted_user = self.repo.get(self.user1.id)  # Attempt to retrieve the deleted user

        # Debugging: Check the deleted user
        print(f"Deleted User: {deleted_user}")

        # Assertions
        self.assertIsNone(deleted_user)

    def test_get_by_attribute(self):
        """Test retrieving an object by an attribute"""
        self.repo.add(self.user1)  # Add user1 to the repository
        self.repo.add(self.user2)  # Add user2 to the repository

        # Retrieve a user by their email
        retrieved_user = self.repo.get_by_attribute("email", "bob@example.com")

        # Debugging: Check the retrieved user
        print(f"User retrieved by email: {retrieved_user}")

        # Assertions
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.first_name, "Bob") # type: ignore


if __name__ == "__main__":
    unittest.main()