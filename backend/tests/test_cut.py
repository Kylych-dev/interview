import pytest
from functools import partial
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase
from apps.cut.models import Cut
from .factories import (
    OrderFactory,
    WarehouseFactory,
    SewingWorkshopFactory,
    ClientFactory,
    CustomUserFactory,
    CutFactory,
)
from utils import OrderStatus


@pytest.mark.skip
@mark.django_db
class TestCut(APITestCase):
    def setUp(self):
        self.url: str = reverse("cut-create")
        self.detail_url: str = partial(reverse, "cut-update")
        self.list_url: str = reverse("cut-list")

    def test_cut_create(self):
        sewing_workshop = SewingWorkshopFactory()
        warehouse = WarehouseFactory(sewing_workshop=sewing_workshop)
        client = ClientFactory()
        order = OrderFactory(warehouse=warehouse, client=client)
        payload = {"name": "skirt"}
        self.assertEqual(Cut.objects.count(), 1)
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(5):
            res = self.client.post(self.url, data=payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_cut_update(self):
        sewing_workshop = SewingWorkshopFactory()
        warehouse = WarehouseFactory(sewing_workshop=sewing_workshop)
        client = ClientFactory()
        order = OrderFactory(warehouse=warehouse, client=client)
        payload = {"order": order.id, "name": "skirt"}
        cut = CutFactory(order=order)
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(6):
            res = self.client.put(self.detail_url(kwargs={"pk": cut.id}), data=payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            order.refresh_from_db()

    def test_list_cut(self):
        client = ClientFactory()
        sewing_workshop = SewingWorkshopFactory()
        warehouse = WarehouseFactory(sewing_workshop=sewing_workshop)
        order = OrderFactory(warehouse=warehouse, client=client)
        cuts = [CutFactory(order=order)]
        sewing_workshop = SewingWorkshopFactory()
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(3):
            res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertEqual(len(res_json), len(cuts))
