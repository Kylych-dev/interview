import pytest
from functools import partial
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import CustomUserFactory, WarehouseMaterialFactory, MaterialTemplate

@pytest.mark.skip
@mark.django_db
class TestWarehouseMaterial(APITestCase):
    def setUp(self):
        self.url: str = reverse("warehousematerial-create")
        self.detail_url: str = partial(reverse, "warehousematerial-update")
        self.list_url: str = reverse("warehousematerial-list")

    def test_warehouse_material_list(self):
        user = CustomUserFactory()
        material = MaterialTemplate()
        warehouse_materials = [WarehouseMaterialFactory(material=material)]
        self.client.force_login(user)
        with self.assertNumQueries(5):
            res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertEqual(len(res_json), len(warehouse_materials))
