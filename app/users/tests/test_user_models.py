from django.contrib.auth import get_user_model
from django.test import TestCase


class LogInTest(TestCase):
    def setUp(self):
        self.email = 'test@test.com'
        self.username = 'testuser'
        self.password = 'Password123'
        self.default_test_user = get_user_model().objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )

    def test_login_via_username(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in)
        
    def test_login_via_mail(self):
        logged_in = self.client.login(email=self.email, password=self.password)
        self.assertTrue(logged_in)


class ModelsTest(TestCase):
    def setUp(self):
        self.email = 'test@test.com'
        self.username = 'testuser'
        self.password = 'Password123'
        self.default_test_user = get_user_model().objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        user = get_user_model().objects.create_user(
            'test@test.com',
            'test123'
        )

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        self.assertEqual(self.default_test_user.email, self.email.lower())

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
