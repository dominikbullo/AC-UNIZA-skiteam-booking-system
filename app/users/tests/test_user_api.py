import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class ProfileViewSetTestCase(APITestCase):
    list_url = reverse("profile-list")

    def setUp(self):
        """Test creating user with valid payload is successful"""
        self.payload = {
            "username": "testuser",
            "email": "test@test.sk",
            "password": "testpass"
        }
        self.user = create_user(**self.payload)
        self.token = Token.objects.get(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse("profile-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.payload["email"])

    def test_profile_update_by_owner(self):
        data = {
            "id": 1,
            "user": self.payload["email"],
            "location": "Anchiano",
            "phone_number": "0902111111",
            "avatar": None,
            'birth_date': None,
            'user_type': None
        }
        change = {"location", "phone_number"}

        response = self.client.put(reverse("profile-detail", kwargs={"pk": 1}),
                                   {key: data[key] for key in set(change) & set(data)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_profile_update_by_random_user(self):
        payload = {
            "username": "random",
            "email": "random@test.sk",
            "password": "testpass"
        }
        random_user = create_user(**payload)
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("profile-detail", kwargs={"pk": 1}), {"location": "hacked!!!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
# from rest_framework.test import APIClient
# from rest_framework import status
#
# TOKEN_URL = reverse("token")
# ME_URL = reverse("me")
#
#
# def create_user(**params):
#     return get_user_model().objects.create_user(**params)
#
#
# class PublicUserApiTests(TestCase):
#     """Test the users API (public)"""
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_create_valid_user_success(self):
#         """Test creating user with valid payload is successful"""
#         payload = {
#             "username": "testuser",
#             "email": "test@test.sk",
#             "password": "testpass"
#         }
#         create_user(**payload)
#
#     # def test_user_exists(self):
#     #     """Test creatinga  user that already exists fails"""
#     #     payload = {"email": "test@test.sk", "password": "testpass"}
#     #     create_user(**payload)
#
#     def test_password_too_short(self):
#         """Test that the password must be more than 5 characters"""
#         payload = {"email": "test@test.sk", "password": "pw"}
#         # res = self.client.post(CREATE_USER_URL, payload)
#
#         # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         user_exists = get_user_model().objects.filter(
#             email=payload["email"]
#         ).exists()
#         self.assertFalse(user_exists)
#
#     def test_create_token_no_user(self):
#         """Test that token is not created if user doesn"t exist"""
#         payload = {"email": "test@test.sk", "password": "testpass"}
#         res = self.client.post(TOKEN_URL, payload)
#
#         self.assertNotIn("token", res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_create_token_missing_field(self):
#         """Test that email and password are required"""
#         res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})
#         self.assertNotIn("token", res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_retrieve_user_unauthorized(self):
#         """Test that authentication is required for users"""
#         res = self.client.get(ME_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateUserApiTests(TestCase):
#     """Test API requests that require authentication"""
#
#     def setUp(self):
#         self.user = create_user(
#             email="test@test.sk",
#             password="testpass",
#             name="name"
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#     def test_retrieve_profile_success(self):
#         """Test retrieving profile for logged in used"""
#         res = self.client.get(ME_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {
#             "name": self.user.name,
#             "email": self.user.email
#         })
#
#     def test_post_me_not_allowed(self):
#         """Test that POST is not allowed on the me url"""
#         res = self.client.post(ME_URL, {})
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_update_user_info(self):
#         """Test updating the user profile for authenticated user"""
#         payload = {"name": "new name", "password": "newpassword123"}
#
#         res = self.client.patch(ME_URL, payload)
#
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.name, payload["name"])
#         self.assertTrue(self.user.check_password(payload["password"]))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)


# TODO API profile/user tests
# someone can rewrite profile data
# someone see data which dont want to see
# admin and owner only can rewrite

# TODO API Account handling tests
# get token
# get info
# change info
