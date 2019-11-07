import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        # TODO test
        pass
        # data = {"username": "testcase", "email": "test@localhost.app",
        #         "password1": "some_strong_psw", "password2": "some_strong_psw"}
        # response = self.client.post("/api/rest-auth/registration/", data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
