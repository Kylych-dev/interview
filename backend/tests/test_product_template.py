from functools import partial
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase
from apps.warehouse.models import ProductTemplate
from utils import SizeChoices
from .factories import ProductTemplateFactory, CustomUserFactory, SewingWorkshopFactory


@mark.django_db
class TestProductTemplate(APITestCase):
    def setUp(self):
        self.url: str = reverse("product-template-create")
        self.detail_url: str = partial(reverse, "product-template-update")
        self.list_url: str = reverse("product-template-list")

    def test_product_template_create(self):
        payload = {"name": "Dress", "color": "Blue", "size": SizeChoices.S}
        self.assertEqual(ProductTemplate.objects.count(), 0)
        sewing_workshop = SewingWorkshopFactory()
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(5):
            res = self.client.post(self.url, data=payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            new_product_template = ProductTemplate.objects.first()
            self.assertEqual(new_product_template.name, payload["name"])
            self.assertEqual(new_product_template.color, payload["color"])
            self.assertEqual(new_product_template.size, payload["size"])

    def test_product_template_update(self):
        payload = {"name": "Dress", "color": "Blue", "size": SizeChoices.M}
        product_template = ProductTemplateFactory()
        sewing_workshop = SewingWorkshopFactory()
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(6):
            res = self.client.put(self.detail_url(kwargs={"pk": product_template.id}), data=payload)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            product_template.refresh_from_db()
            self.assertEqual(product_template.name, payload["name"])
            self.assertEqual(product_template.color, payload["color"])
            self.assertEqual(product_template.size, payload["size"])

    def test_product_template_item(self):
        product_templates = [ProductTemplateFactory()]
        sewing_workshop = SewingWorkshopFactory()
        user = CustomUserFactory(sewing_workshop=sewing_workshop)
        self.client.force_login(user)
        with self.assertNumQueries(3):
            res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertEqual(len(res_json), len(product_templates))
