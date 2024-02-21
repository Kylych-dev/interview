from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.cut.models import Cut
from utils import OrderStatus


@receiver(post_save, sender=Cut)
def order_status_change(sender, instance, created, **kwargs):
    if instance.is_ready and instance.order.status == OrderStatus.CUTTING:
        instance.order.status = OrderStatus.PRODUCTION
        instance.order.save()
