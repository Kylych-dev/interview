from functools import partial
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase
from apps.warehouse.models import MaterialTemplate
from .factories import CustomUserFactory, MaterialTemplateFactory
from utils import UnitChoices


@mark.django_db
class TestMaterialTemplate(APITestCase):
    def setUp(self):
        self.url: str = reverse("material-create")
        self.detail_url: str = partial(reverse, "material-update")
        self.list_url: str = reverse("material-list")

    def test_material_template_create(self):
        payload = {"name": "Dress", "unit": UnitChoices.PIECE, "color": "Blue"}

        user = CustomUserFactory()
        self.client.force_login(user)
        self.assertEqual(MaterialTemplate.objects.count(), 0)
        with self.assertNumQueries(4):
            res = self.client.post(self.url, data=payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            material_template = MaterialTemplate.objects.first()
            self.assertEqual(material_template.name, payload["name"])
            self.assertEqual(material_template.unit, payload["unit"])
            self.assertEqual(material_template.color, payload["color"])

    def test_update_material_template(self):
        payload = {"name": "Dress", "unit": UnitChoices.PIECE, "color": "Blue"}
        material_template = MaterialTemplateFactory()
        user = CustomUserFactory()
        self.client.force_login(user)
        self.assertEqual(MaterialTemplate.objects.count(), 1)
        with self.assertNumQueries(5):
            res = self.client.put(
                self.detail_url(kwargs={"pk": material_template.id}), data=payload
            )
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            material_template.refresh_from_db()
            self.assertEqual(material_template.name, payload["name"])
            self.assertEqual(material_template.color, payload["color"])
            self.assertEqual(material_template.unit, payload["unit"])

    def test_list_material_template(self):
        material_templates = [MaterialTemplateFactory()]
        user = CustomUserFactory()
        self.client.force_login(user)
        with self.assertNumQueries(3):
            res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = res.json()
        self.assertEqual(len(res_json), len(material_templates))
