# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
#
# from users.tests.test_auth_api import get_default_user
#
# CREATE_CHILD_URL = reverse('family:child-list')
# LOGIN_USER_URL = reverse('rest_login')
#
# default_payload = {
#     "user": {
#         "username"  : "testUsername",
#         "password1" : "testing321",
#         "password2" : "testing321",
#         "first_name": "TestName",
#         "last_name" : "TestSurname",
#         "profile"   : {
#             "birth_date": "09.12.1996",
#             "gender"    : "M"
#         }
#     }
# }
#
#
# # FIXME -> create child with parent token or info
# def create_child(payload=None):
#     if payload is None:
#         payload = default_payload
#     return APIClient().post(CREATE_CHILD_URL, payload, format='json')
#
#
# def get_child(res):
#     payload = {
#         "id"        : res.data["user"].get("id", None),
#         "username"  : res.data["user"].get("username", None),
#         "email"     : res.data["user"].get("email", None),
#         "first_name": res.data["user"].get("first_name", None),
#         "last_name" : res.data["user"].get("last_name", None),
#     }
#     return get_user_model().objects.get(**payload)
#
#
# def get_default_child():
#     return get_child(create_child())
#
#
# class RegisterChildApiTests(APITestCase):
#     def setUp(self):
#         self.parent = get_default_user()
#         self.payload = default_payload
#
#     def test_create_child_only_username_successful(self):
#         """Test creating a new user with an email is successful"""
#         res = create_child()
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         user = get_child(res)
#         self.assertTrue(user.check_password(self.payload['password1']))
#         self.assertNotIn('password', res.data)
#
#
# class LoginUserApiTests(APITestCase):
#     # TODO Login user with mail
#     # TODO Login user with username
#     # TODO Login unverified
#     def setUp(self):
#         self.user = get_child(create_child())
#
#         self.payload = {
#             "email"   : default_payload.get("email", None),
#             "password": default_payload.get("password1", None)
#         }
#
#     def test_login_user_with_email_success(self):
#         res = self.client.post(LOGIN_USER_URL, self.payload, format='json')
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#     def test_login_wrong_email(self):
#         payload = {
#             "email"   : "non@working.email",
#             "password": default_payload.get("password1", None)
#         }
#         res = self.client.post(LOGIN_USER_URL, payload, format='json')
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_login_wrong_pass(self):
#         payload = {
#             "email"   : default_payload.get("email", None),
#             "password": "not right password"
#         }
#         res = self.client.post(LOGIN_USER_URL, payload, format='json')
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_login_email_into_username_field_success(self):
#         payload = {
#             "username": default_payload.get("email", None),
#             "password": default_payload.get("password1", None)
#         }
#         res = self.client.post(LOGIN_USER_URL, payload, format='json')
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#     def test_normalized_email(self):
#         payload = self.payload
#         payload["email"] = payload["email"].upper()
#
#         res = self.client.post(LOGIN_USER_URL, payload, format='json')
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
