from functools import partial
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase
from apps.warehouse.models import Product
from .factories import (
    CustomUserFactory,
    ProductTemplateFactory,
    CutFactory,
    WarehouseFactory,
    SewingWorkshopFactory,
    ProductFactory,
)
# todo: Кылыч перделать тесты

@mark.django_db
class TestProduct(APITestCase):
    def setUp(self):
        self.url: str = reverse("product-create")
        self.detail_url: str = partial(reverse, "product-update")
        self.list_url: str = reverse("product-list")

    def test_product_create(self):
        sewing_workshop = SewingWorkshopFactory()
        product_template = ProductTemplateFactory()
        cut = CutFactory()
        warehouse = WarehouseFactory()
        payload = {
            "product_template": product_template.id,
            "quantity": 50,
            "cost": 100,
            "code": "code",
            "cut": cut.id,
            "warehouse": warehouse.id,
            "seamstress": 50,
            "technologist": 200,
            "iron_worker": 70,
            "button_attacher": 100,
            "button": 20,
            "packer": 50,
            "is_active": False,
        }
        self.assertEqual(Product.objects.count(), 0)
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(10):
            res = self.client.post(self.url, data=payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            new_product = Product.objects.first()
            self.assertEqual(new_product.product_template.id, payload["product_template"])
            self.assertEqual(new_product.quantity, payload["quantity"])
            self.assertEqual(new_product.cost, payload["cost"])
            self.assertEqual(new_product.cut.id, payload["cut"])
            self.assertEqual(new_product.warehouse.id, payload["warehouse"])
            self.assertEqual(new_product.seamstress, payload["seamstress"])
            self.assertEqual(new_product.technologist, payload["technologist"])
            self.assertEqual(new_product.iron_worker, payload["iron_worker"])
            self.assertEqual(new_product.button_attacher, payload["button_attacher"])
            self.assertEqual(new_product.button, payload["button"])
            self.assertEqual(new_product.packer, payload["packer"])
            self.assertEqual(new_product.is_active, payload["is_active"])

    def test_update_product(self):
        sewing_workshop = SewingWorkshopFactory()
        product_template = ProductTemplateFactory()
        cut = CutFactory()
        warehouse = WarehouseFactory()
        product = ProductFactory(product_template=product_template, warehouse=warehouse, cut=cut)
        payload = {
            "product_template": product_template.id,
            "quantity": 960,
            "cost": 100,
            "code": "code",
            "cut": cut.id,
            "warehouse": warehouse.id,
            "seamstress": 50,
            "technologist": 200,
            "iron_worker": 70,
            "button_attacher": 100,
            "button": 20,
            "packer": 50,
            "is_active": False,
        }
        self.assertEqual(Product.objects.count(), 1)

        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(11):
            res = self.client.put(
                self.detail_url(kwargs={"pk": product.id}), data=payload
            )
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            product.refresh_from_db()
            self.assertEqual(product.product_template.id, payload["product_template"])
            self.assertEqual(product.quantity, payload["quantity"])
            self.assertEqual(product.cost, payload["cost"])
            self.assertEqual(product.cut.id, payload["cut"])
            self.assertEqual(product.warehouse.id, payload["warehouse"])
            self.assertEqual(product.seamstress, payload["seamstress"])
            self.assertEqual(product.technologist, payload["technologist"])
            self.assertEqual(product.iron_worker, payload["iron_worker"])
            self.assertEqual(product.button_attacher, payload["button_attacher"])
            self.assertEqual(product.button, payload["button"])
            self.assertEqual(product.packer, payload["packer"])
            self.assertEqual(product.is_active, payload["is_active"])

    def test_list_product(self):
        sewing_workshop = SewingWorkshopFactory()
        product_template = ProductTemplateFactory()
        cut = CutFactory()
        warehouse = WarehouseFactory()
        products = [ProductFactory(product_template=product_template, warehouse=warehouse, cut=cut)]
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(3):
            res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertEqual(len(res_json), len(products))
