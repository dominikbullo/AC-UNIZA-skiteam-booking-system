from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase

from core.utils import create_user, update_username_from_email_for_testing


class LogInTest(TestCase):
    def setUp(self):
        email = "test@test.com"
        # because i'am changing username in signals! This is really important,
        # because when i want to create user, I need username
        username = update_username_from_email_for_testing(email)

        self.credentials = {
            "email": email,
            "username": username,
            "password": "Password123"
        }
        self.user = create_user(**self.credentials)

    def tearDown(self):
        self.user.delete()

    def test_changing_username(self):
        self.assertEqual(self.user.username, self.credentials["username"])

    # def test_generating_original_custom_username(self):
    #     username1 = update_username_from_email_for_testing(self.credentials["email"])
    #     user1 = create_user(**self.credentials)
    #
    #     self.assertNotEqual(user1.username, self.credentials["username"])
    #     self.assertEqual(user1.username, username1)

    def test_login_via_username(self):
        logged_in = self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        self.assertTrue(logged_in)

    def test_login_via_mail(self):
        logged_in = self.client.login(email=self.credentials['email'], password=self.credentials['password'])
        self.assertTrue(logged_in)

    def test_correct(self):
        user = authenticate(username=self.credentials['username'], password=self.credentials['password'])
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password=self.credentials['password'])
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username=self.credentials['username'], password='definitelynotrightpass')
        self.assertFalse(user is not None and user.is_authenticated)


class ModelsTest(TestCase):
    def setUp(self):
        self.credentials = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "Password123"
        }
        self.default_test_user = create_user(**self.credentials)

    # def test_create_user_with_email_successful(self):
    #     credentials = {
    #         "username": "test@test.com",
    #         "password": "Password123"
    #     }
    #     user = create_user(**credentials)
    #     logged_in = self.client.login(username=credentials['username'], password=credentials['password'])
    #     self.assertTrue(logged_in)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        self.assertEqual(self.default_test_user.email, self.credentials['email'].lower())

    def test_new_user_invalid_username(self):
        """Test creating user with no username raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(username=None, email="test@test.sk", password="test123")

    # TODO test without mail raise error
    # def test_new_user_invalid_email(self):
    #     """Test creating user with no email raises error"""
    #     with self.assertRaises(ValueError):
    #         get_user_model().objects.create_user(username="testusername", email=None, password="test123")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'superuser',
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

# TODO User account tests
# Registration
# Reg without some parameters
# Reg via API -> shoud be not possible
# Reg via browser
