from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.warehouse.models import MaterialIncome
from apps.warehouse.models.warehouse import MaterialCutOutcome, MaterialOutcomeHistory
from utils import OrderStatus


@transaction.atomic
@receiver(post_save, sender=MaterialIncome)
def material_income_changes(sender, instance, created, **kwargs):
    if created:
        instance.material.quantity += instance.quantity
        instance.material.save()


@transaction.atomic
@receiver(post_save, sender=MaterialCutOutcome)
def change_order_status(sender, instance, created, **kwargs):
    if instance.is_ready and instance.cut.order.status == OrderStatus.WAREHOUSE:
        instance.cut.order.status = OrderStatus.CUTTING
        instance.cut.order.save()


@transaction.atomic
@receiver(post_save, sender=MaterialOutcomeHistory)
def add_outcome_for_material_history(sender, instance, created, **kwargs):
    if created:
        if instance.material.quantity < instance.quantity:
            raise ValueError("Сумма расхода больше чем есть на складе")

        instance.material.quantity -= instance.quantity
        instance.material.save(update_fields=["quantity"])