from django.test import TestCase
from rest_framework.test import APIClient
from .models import CustomUser


class CustomUserModelTestCase(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create_user(
            email="test@example.com", password="test123"
        )
        self.assertEqual(user.email, "test@example.com")


class CustomUserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {"email": "test@example.com", "password": "test123"}
        response = self.client.post("/api/v1/register/", data)
        self.assertEqual(response.status_code, 201)

    def test_token_obtain(self):
        user = CustomUser.objects.create_user(
            email="test@example.com", password="test123"
        )
        data = {"email": "test@example.com", "password": "test123"}
        response = self.client.post("/api/v1/token/", data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
