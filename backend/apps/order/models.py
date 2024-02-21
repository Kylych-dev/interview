from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import CustomUser, UserRole
from apps.client.models import Client
from apps.warehouse.models.warehouse import Warehouse
from utils import OrderStatus


class Order(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.DO_NOTHING,
        related_name="order",
        verbose_name=_("Склад"),
    )
    name = models.CharField(
        "Название заказа", max_length=300
    )
    product_category = models.ForeignKey(
        "ProductCategory",
        on_delete=models.DO_NOTHING,
        verbose_name='Категория продукта',
        related_name='order',
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Клиент"),
        related_name="order",
    )
    quantity = models.PositiveIntegerField(
        _("Общее количество товара"),
    )
    photo = models.ImageField(
        upload_to="products_photos/",
        verbose_name=_("Изображение"),
        null=True,
        blank=True,
    )
    comment = models.TextField(verbose_name=_("Комментарий"))
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.START,
        max_length=30,
        verbose_name=_("Статус заказа"),
    )
    start_order = models.DateField(
        verbose_name="Дата запуска",
    )
    end_order = models.DateField(
        verbose_name="Срок сдачи",
    )
    is_ready = models.BooleanField("Запустить в продукцию", default=False)
    is_done = models.BooleanField(
        "Заказ отправлен заказчику",
        default=False,
        help_text="Поле заполняется в конце процесса",
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)
    update_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.client.full_name} - {self.get_status_display()}"

    def change_status(self, status):
        self.status = status
        self.save()

    class Meta:
        verbose_name = "1. Заказ"
        verbose_name_plural = "1. Заказы"


class ProductCategory(models.Model):
    """
    Модель для представления категории товара.

    Пример: Футболка, Брюки
    """

    name = models.CharField(
        verbose_name=_("Название продукта"),
        help_text="Пример: Футболка, Брюки и т.д",
        max_length=255, unique=True,
    )
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Образец Продукта"
        verbose_name_plural = "Образцы Продукта"


class Payment(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Заказ"),
    )
    role = models.ForeignKey(
        UserRole,
        on_delete=models.CASCADE,
        verbose_name=_("Должность"),
        related_name="payments",
    )
    amount = models.DecimalField(
        verbose_name=_("Цена за шт."),
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"Платеж для заказа: {self.order.name}, для роли: {self.role.role_name}"

    class Meta:
        verbose_name = _("Платеж")
        verbose_name_plural = _("Платежи")
