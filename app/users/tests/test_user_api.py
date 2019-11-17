from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

# # TODO Tests for API calls (get user info, Profile update and so on)
# class ProfileViewSetTestCase(APITestCase):
#     list_url = reverse("profile-list")
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username="davinci",
#                                                          password="some-very-strong-psw")
#         self.token = Token.objects.create(user=self.user)
#         self.api_authentication()
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
#
#     def test_profile_list_authenticated(self):
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_profile_list_un_authenticated(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# def test_profile_update_by_owner(self):
#     response = self.client.put(reverse("profile-detail", kwargs={"pk": 1}),
#                                {"city": "Anchiano", "bio": "Renaissance Genius"})
#     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     self.assertEqual(json.loads(response.content),
#                      {"id": 1, "user": "davinci", "bio": "Renaissance Genius",
#                       "city": "Anchiano", "avatar": None})

# def test_profile_update_by_random_user(self):
#     random_user = User.objects.create_user(username="random",
#                                            password="psw123123123")
#     self.client.force_authenticate(user=random_user)
#     response = self.client.put(reverse("profile-detail", kwargs={"pk": 1}),
#                                {"bio": "hacked!!!"})
#     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
