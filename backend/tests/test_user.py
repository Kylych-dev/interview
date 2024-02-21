from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase
from utils import Role
from apps.accounts.models import CustomUser


@mark.django_db
class TestCustomerUser(APITestCase):
    def setUp(self):
        self.register_url: str = reverse("register")

    def test_user_registration(self):
        payload = {
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "password": "Testpassword!",
            "password2": "Testpassword!",
            "role": Role.SEAMSTRESS,
            "phone_number": "+996111222444",
        }
        self.assertEqual(CustomUser.objects.count(), 0)

        with self.assertNumQueries(2):
            res = self.client.post(self.register_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        new_user = CustomUser.objects.first()
        self.assertEqual(new_user.first_name, payload["first_name"])
        self.assertEqual(new_user.last_name, payload["last_name"])
        self.assertEqual(new_user.role, payload["role"])
        self.assertEqual(new_user.phone_number, payload["phone_number"])
