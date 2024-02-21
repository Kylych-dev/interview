from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import CustomUser
from apps.fabrication.models import FabricationMoveStatus, Fabrication
from apps.wallet.models import Transaction
from utils import ProductStatus, Role, OrderStatus


@receiver(post_save, sender=FabricationMoveStatus)
def fabrication_pay_for_worker(sender, instance, created, **kwargs):
    if created:
        instance.seamstress_id = instance.worker_id
        if instance.product.quantity < instance.count:
            raise ValueError("Уменьшите количество производимых продукций")

        instance.product.quantity -= instance.count
        instance.product.save()
        instance.save()

    if instance.worker and instance.worker.role in [
        Role.WAREHOUSEMAN,
        Role.CUTTER,
    ]:
        raise ValueError("Для такого пользователя нельзя добавлять статус работы")

    if instance.send_to and instance.status == ProductStatus.PACKER:
        instance.status = ProductStatus.COMPLETED
        instance.save()

    if instance.send_to and instance.worker_to and instance.accept_from:
        if instance.status == ProductStatus.SEAMSTRESS:
            instance.status = ProductStatus.TECHNOLOGIST
        elif instance.status == ProductStatus.TECHNOLOGIST:
            instance.status = ProductStatus.OTK
        elif instance.status == ProductStatus.OTK:
            instance.status = ProductStatus.IRON_WORKER
        elif instance.status == ProductStatus.IRON_WORKER:
            instance.status = ProductStatus.PACKER

        instance.send_to = False
        instance.accept_from = False
        instance.worker = instance.worker_to
        instance.worker_to = None
        instance.save()

    if instance.status == ProductStatus.IRON_WORKER:
        seamstress = CustomUser.objects.get(pk=instance.seamstress_id)
        price = getattr(instance.product, seamstress.role)
        summ = price * instance.count
        Transaction.objects.create(
            wallet=seamstress.employeewallet,
            amount=summ,
            description=f"Пользователь {seamstress} - выполнил {instance.product}"
            f" в количестве {instance.count} шт. на сумму {summ} сом",
        )


@receiver(post_save, sender=Fabrication)
def fabrication_order_status(sender, instance, created, **kwargs):
    if instance.is_ready and instance.order.status == OrderStatus.PRODUCTION:
        instance.order.status = OrderStatus.READY
        instance.order.save()
