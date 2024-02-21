from functools import partial
from django.urls import reverse
from pytest import mark
from rest_framework import status
from apps.client.models import Client
from rest_framework.test import APITestCase
from utils.constants import Role
from .factories import CustomUserFactory, ClientFactory


@mark.django_db
class TestOrder(APITestCase):
    def setUp(self):
        self.url: str = reverse("client-create")
        self.detail_url: str = partial(reverse, "client-update")
        self.list_url: str = reverse("client-list")

    def test_client_create_as_director(self):
        payload = {
            "full_name": "TestUser",
            "phone_number": "+996111222333",
            "address": "Bishkek",
        }

        user = CustomUserFactory(role=Role.DIRECTOR)
        self.client.force_login(user)
        self.assertEqual(Client.objects.count(), 0)
        with self.assertNumQueries(8):
            res = self.client.post(self.url, data=payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            new_client = Client.objects.first()
            self.assertEqual(new_client.warehouse.id, user.sewing_workshop.warehouse.id)
            self.assertEqual(new_client.full_name, payload["full_name"])
            self.assertEqual(new_client.phone_number, payload["phone_number"])
            self.assertEqual(new_client.address, payload["address"])

    def test_client_update(self):
        user = CustomUserFactory(role=Role.DIRECTOR)
        client = ClientFactory(warehouse=user.sewing_workshop.warehouse)
        payload = {
            "full_name": "TestUser",
            "phone_number": "+996111222333",
            "address": "Bishkek",
        }

        self.client.force_login(user)
        self.assertEqual(Client.objects.count(), 1)
        with self.assertNumQueries(9):
            res = self.client.put(
                self.detail_url(kwargs={"pk": client.id}), data=payload
            )
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(Client.objects.count(), 1)
            client.refresh_from_db()
            self.assertEqual(client.full_name, payload["full_name"])
            self.assertEqual(client.phone_number, payload["phone_number"])
            self.assertEqual(client.address, payload["address"])

    def test_client_list(self):
        user = CustomUserFactory()
        clients = [ClientFactory(warehouse=user.sewing_workshop.warehouse)]

        self.client.force_login(user)
        with self.assertNumQueries(5):
            res = self.client.get(self.list_url)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            res_json = res.json()
            self.assertEqual(len(res_json), len(clients))
