# from django.test import TestCase
# from rest_framework import status
#
#
# class AccountHandling(TestCase):
#     def test_signup_form(self):
#         credentials = {
#             "email": "test@test.sk",
#             "password1": "testpass",
#             "password2": "testpass",
#             "first_name": "First",
#             "last_name": "LAst"
#         }
#         response = self.client.post("/signup/", credentials)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_signup_form_without_email(self):
#         credentials = {
#             "password1": "testpass",
#             "password2": "testpass",
#             "first_name": "First",
#             "last_name": "LAst"
#         }
#         response = self.client.post("/signup/", **credentials)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

# TODO Forms test
# validation of form
# right messages
# anti spam
