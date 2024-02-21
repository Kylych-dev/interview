from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.order.models import Order


class Cut(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name=_("Заказ"), related_name="cut"
    )
    is_ready = models.BooleanField(verbose_name=_("Готовность кроя"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)

    def __str__(self):
        return (
            f"Крой {self.order.name} созданный от {self.created_at.strftime('%d.%m.%Y %H:%M')} "
            f"Необходимо создать - {self.order.quantity} шт."
        )

    class Meta:
        verbose_name = "3. Крой"
        verbose_name_plural = "3. Крой"
