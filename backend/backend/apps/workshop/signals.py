from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.warehouse.models.warehouse import Warehouse
from apps.workshop.models import SewingWorkshop


@receiver(post_save, sender=SewingWorkshop)
def sewing_workshop_warehouse_create(sender, instance, created, **kwargs):
    if created:
        Warehouse.objects.create(sewing_workshop=instance)
