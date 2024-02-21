from functools import partial
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase
from apps.order.models import Order
from .factories import (
    CustomUserFactory,
    SewingWorkshopFactory,
    ClientFactory,
    WarehouseFactory,
    OrderFactory,
)
from utils.constants import Status


@mark.django_db
class TestOrder(APITestCase):
    def setUp(self):
        self.url: str = reverse("order-create")
        self.detail_url: str = partial(reverse, "order-update")
        self.list_url: str = reverse("order-list")

    def test_order_create(self):
        sewing_workshop = SewingWorkshopFactory()
        warehouse = WarehouseFactory(sewing_workshop=sewing_workshop)
        client = ClientFactory(warehouse=warehouse)
        payload = {
            "client": client.id,
            "name": "string",
            "comment": "string",
            "quantity": 922,
            "status": "start",
            "is_done": False,
            "start_order": "2023-12-12",
            "end_order": "2023-12-14",
        }

        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        self.assertEqual(Order.objects.count(), 0)
        with self.assertNumQueries(13):
            res = self.client.post(self.url, data=payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            new_order = Order.objects.first()
            self.assertEqual(new_order.warehouse.id, user.sewing_workshop.warehouse.id)
            self.assertEqual(new_order.client.id, payload["client"])
            self.assertEqual(new_order.name, payload["name"])
            self.assertEqual(new_order.comment, payload["comment"])
            self.assertEqual(new_order.quantity, payload["quantity"])
            self.assertEqual(new_order.status, payload["status"])

    def test_order_update(self):
        sewing_workshop = SewingWorkshopFactory()
        warehouse = WarehouseFactory(sewing_workshop=sewing_workshop)
        client = ClientFactory(warehouse=warehouse)
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        order = OrderFactory(client=client, warehouse=user.sewing_workshop.warehouse)
        payload = {
            "client": client.id,
            "name": "string",
            "comment": "string",
            "quantity": 922,
            "status": "start",
            "is_done": False,
            "start_order": "2023-12-12",
            "end_order": "2023-12-13",
        }

        self.assertEqual(Order.objects.count(), 1)
        self.client.force_login(user)
        with self.assertNumQueries(9):
            res = self.client.put(
                self.detail_url(kwargs={"pk": order.id}), data=payload
            )
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(Order.objects.count(), 1)
            order.refresh_from_db()
        self.assertEqual(order.client.id, payload["client"])
        self.assertEqual(order.name, payload["name"])
        self.assertEqual(order.comment, payload["comment"])
        self.assertEqual(order.quantity, payload["quantity"])
        self.assertEqual(order.status, payload["status"])

    def test_order_list(self):
        sewing_workshop = SewingWorkshopFactory()
        warehouse = WarehouseFactory(sewing_workshop=sewing_workshop)
        client = ClientFactory(warehouse=warehouse)
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        orders = [
            OrderFactory(
                client=client, warehouse=user.sewing_workshop.warehouse, status=value
            )
            for value in Status.values
        ]

        self.client.force_login(user)
        with self.assertNumQueries(5):
            res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertEqual(len(res_json), len(orders))
