from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.cut.models import Cut
from apps.fabrication.models import Fabrication
from apps.order.models import Order
from apps.warehouse.models.warehouse import (
    MaterialCutOutcome,
    MaterialFabricationOutcome,
)
from utils import OrderStatus


@receiver(post_save, sender=Order)
def order_status_change(sender, instance, created, **kwargs):
    if created:
        cut = Cut.objects.create(order=instance)
        fabrication = Fabrication.objects.create(order=instance)
        MaterialCutOutcome.objects.create(cut=cut)
        MaterialFabricationOutcome.objects.create(fabric=fabrication)

    if instance.is_ready and instance.status == OrderStatus.START:
        Order.objects.filter(pk=instance.pk).update(status=OrderStatus.WAREHOUSE)

    if instance.is_done and instance.status == OrderStatus.READY:
        Order.objects.filter(pk=instance.pk).update(status=OrderStatus.COMPLETED)
