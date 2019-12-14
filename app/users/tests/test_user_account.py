from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase

from core.utils import create_user


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "Password123"
        }
        self.user = create_user(**self.credentials)

    def tearDown(self):
        self.user.delete()

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

    def test_wrong_pssword(self):
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

    def test_create_user_with_email_successful(self):
        credentials = {
            "username": "test@test.com",
            "password": "Password123"
        }
        create_user(**credentials)
        logged_in = self.client.login(username=credentials['username'], password=credentials['password'])
        self.assertTrue(logged_in)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        self.assertEqual(self.default_test_user.email, self.credentials['email'].lower())

    def test_new_user_invalid_username(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test@test.sk", 'test123')

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
# what if user dont have username
# TODO user must have username when admin is creating him manually
