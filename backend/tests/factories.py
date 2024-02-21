import datetime
import factory
from django.db.models.signals import post_save
from django.utils.timezone import now
from factory import fuzzy
from apps.order.models import Order
from apps.fabrication.models import Fabrication
from apps.client.models import Client
from apps.warehouse.models import (
    MaterialTemplate,
    Warehouse,
    WarehouseMaterial,
)
from apps.cut.models import Cut
from django.contrib.auth import get_user_model
from utils import SizeChoices, OrderStatus, Role, UnitChoices
from apps.workshop.models import SewingWorkshop


class SewingWorkshopFactory(factory.django.DjangoModelFactory):
    """Фабрика для представления швейного цеха."""

    name = factory.Faker("word")
    slug = factory.Sequence(lambda x: f"slug_{x}")
    phone_number = "+996111222333"

    class Meta:
        model = SewingWorkshop


@factory.django.mute_signals(post_save)
class WarehouseFactory(factory.django.DjangoModelFactory):
    """Фабрика склада"""

    sewing_workshop = factory.SubFactory(SewingWorkshopFactory)
    created_at = now() - datetime.timedelta(days=1)
    updated_at = now()

    class Meta:
        model = Warehouse
        django_get_or_create = ("sewing_workshop",)


class ClientFactory(factory.django.DjangoModelFactory):
    """Фабрика клиента"""

    full_name = factory.Faker("first_name")
    phone_number = "+996222111333"
    address = factory.Faker("address")
    warehouse = factory.SubFactory(WarehouseFactory)

    class Meta:
        model = Client


# class ProductTemplateFactory(factory.django.DjangoModelFactory):
#     """Фабрика модели"""
#
#     name = factory.Faker("word")
#     color = factory.Faker("color_name")
#     size = fuzzy.FuzzyChoice(choices=SizeChoices.values)
#
#     class Meta:
#         model = ProductTemplate


class OrderFactory(factory.django.DjangoModelFactory):
    """Фабрика заказа"""

    warehouse = factory.SubFactory(WarehouseFactory)
    name = factory.Faker("word")
    client = factory.SubFactory(ClientFactory)
    comment = factory.Faker("sentence")
    quantity = factory.Faker(provider="pyint", min_value=0, max_value=10000)
    status = fuzzy.FuzzyChoice(choices=OrderStatus.values)
    start_order = now() + datetime.timedelta(days=2)
    end_order = now() + datetime.timedelta(days=2)
    is_ready = False
    is_done = False
    created_at = now() - datetime.timedelta(days=1)
    update_at = now()

    class Meta:
        model = Order


class CutFactory(factory.django.DjangoModelFactory):
    order = factory.SubFactory(OrderFactory)
    is_ready = False
    created_at = now() - datetime.timedelta(days=1)

    class Meta:
        model = Cut


# class ProductFactory(factory.django.DjangoModelFactory):
#     """Фабрика для представления продукции."""
#
#     product_template = factory.SubFactory(ProductTemplateFactory)
#     quantity = factory.Faker(provider="pyint", min_value=0, max_value=2000)
#     cost = factory.Faker(provider="pyint", min_value=0, max_value=10000)
#     code = factory.Faker("word")
#     cut = factory.SubFactory(CutFactory)
#     warehouse = factory.SubFactory(WarehouseFactory)
#     seamstress = factory.Faker(provider="pyint", min_value=0, max_value=10000)
#     technologist = factory.Faker(provider="pyint", min_value=0, max_value=10000)
#     iron_worker = factory.Faker(provider="pyint", min_value=0, max_value=10000)
#     button_attacher = factory.Faker(provider="pyint", min_value=0, max_value=10000)
#     packer = factory.Faker(provider="pyint", min_value=0, max_value=10000)
#     is_active = False
#
#     class Meta:
#         model = Product


# class FabricationFactory(factory.django.DjangoModelFactory):
#     """Фабрика работы производтсва."""
#
#     order = factory.SubFactory(OrderFactory)
#     product = factory.SubFactory(ProductFactory)
#     created_at = now() - datetime.timedelta(days=1)
#     is_ready = False
#
#     class Meta:
#         model = Fabrication


class CustomUserFactory(factory.django.DjangoModelFactory):
    """Фабрика работы сотрудника."""

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = fuzzy.FuzzyChoice(choices=Role.values)
    phone_number = "996777223311"
    sewing_workshop = factory.SubFactory(SewingWorkshopFactory)
    employment_status = 1

    class Meta:
        model = get_user_model()


class MaterialTemplateFactory(factory.django.DjangoModelFactory):
    """Модель для представления характеристик продукта."""

    name = factory.Faker("word")
    unit = fuzzy.FuzzyChoice(choices=UnitChoices.values)
    color = factory.Faker("color")

    class Meta:
        model = MaterialTemplate


class WarehouseMaterialFactory(factory.django.DjangoModelFactory):
    warehouse = factory.SubFactory(WarehouseFactory)
    material = factory.SubFactory(MaterialTemplateFactory)
    quantity = factory.Faker(provider="pyint", min_value=0, max_value=10000)
    is_delete = False

    class Meta:
        model = WarehouseMaterial
