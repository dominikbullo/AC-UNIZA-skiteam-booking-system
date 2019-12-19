from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

CHILD_LIST_URL = reverse('family:child-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_family_list(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(CHILD_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
