import unittest
import os
import sqlite3
from dbcontroller import DBController

class DBControllerTest(unittest.TestCase):
    _test_db_name = 'users_test.db'

    def setUp(self):
        self.db = DBController(self._test_db_name)
        
        # TODO may not have id = 1
        self.db.create_user('testuser', 100)
        self.db.create_item(1, 'testitem', 10.0)

    def tearDown(self):
        del self.db
        os.remove(self._test_db_name)

    def test_create_user(self):
        # Test creating a new user
        user = self.db.get_user('testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser')
        self.assertEqual(user['credits'], 100)

        # Test creating a user with a duplicate username
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_user('testuser', 100)

    def test_get_user(self):
        # Test retrieving an existing user
        user = self.db.get_user('testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser')
        self.assertEqual(user['credits'], 100)

        # Test retrieving a non-existent user
        user = self.db.get_user('nonexistent')
        self.assertIsNone(user)

    def test_create_item(self):
        # Test creating a new item for an existing user
        items = self.db.get_items(1)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'testitem')
        self.assertEqual(items[0]['price'], 10.0)

        # Test creating an item for a non-existent user
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_item(999, 'testitem', 10.0)

    def test_get_items(self):
        # Test retrieving items for an existing user
        items = self.db.get_items(1)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'testitem')
        self.assertEqual(items[0]['price'], 10.0)

        # Test retrieving items for a non-existent user
        items = self.db.get_items(999)
        self.assertEqual(len(items), 0)

    def test_update_item(self):
        # Test updating an existing item
        self.db.update_item(1, 'newname', 20.0)
        items = self.db.get_items(1)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'newname')
        self.assertEqual(items[0]['price'], 20.0)

        # # Test updating a non-existent item
        # with self.assertRaises(sqlite3.IntegrityError):
        #     self.db.update_item(999, 'newname', 20.0)

    def test_add_credits(self):
        # Test adding credits to an existing user
        self.db.add_credits(1, 50)
        user = self.db.get_user('testuser')
        self.assertEqual(user['credits'], 150)

        # # Test adding credits to a non-existent user
        # with self.assertRaises(sqlite3.IntegrityError):
        #     self.db.add_credits(999, 50)

    def test_subtract_credits(self):
        # Test subtracting credits from an existing user with enough credits
        self.db.subtract_credits(1, 50)
        user = self.db.get_user('testuser')
        self.assertEqual(user['credits'], 50)

        # Test subtracting credits from an existing user with not enough credits
        with self.assertRaises(ValueError):
            self.db.subtract_credits(1, 200)
        user = self.db.get_user('testuser')
        self.assertEqual(user['credits'], 50)

        # Test subtracting credits from a non-existent user
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.subtract_credits(999, 50)


if __name__ == '__main__':
    unittest.main()