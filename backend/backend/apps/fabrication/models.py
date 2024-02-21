from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser
from apps.order.models import Order
from apps.product.models import Product
from utils import ProductStatus


class Fabrication(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Заказ"),
        related_name="fabrication",
        null=True,
        blank=True,
    )
    is_ready = models.BooleanField("Готово", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)

    def __str__(self):
        return f"Производство для: {self.order.name} {self.order.created_at.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = _("4. Производство")
        verbose_name_plural = _("4. Производства")


class FabricationMoveStatus(models.Model):
    status = models.CharField(
        choices=ProductStatus.choices,
        default=ProductStatus.SEAMSTRESS,
        max_length=14,
        verbose_name=_("Статус"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name="work_orders",
        verbose_name=_("Продукт"),
        null=True,
        blank=True,
    )
    work_order = models.ForeignKey(
        Fabrication,
        on_delete=models.DO_NOTHING,
        related_name="work_order",
        verbose_name=_("Работа сотрдуника"),
    )
    worker = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Сотрудник работающий над продуктом"),
        related_name="worker",
        null=True,
        blank=True,
    )
    worker_to = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Сотрудник получающий продукт"),
        related_name="worker_to",
        null=True,
        blank=True,
    )
    seamstress_id = models.PositiveIntegerField(
        verbose_name=_("ID швеи"), null=True, blank=True
    )
    count = models.PositiveIntegerField(default=0, verbose_name=_("Количество"))
    send_to = models.BooleanField(default=False, verbose_name="Работа выполнена")
    accept_from = models.BooleanField(default=False, verbose_name="Работа принята")
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)

    def __str__(self):
        return f"Статус сотрудника - {str(self.get_status_display())}"

    class Meta:
        verbose_name = "Статус работы"
        verbose_name_plural = "Статус работы"
