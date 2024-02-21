from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser
from apps.wallet.models import EmployeeWallet


@receiver(post_save, sender=CustomUser)
def create_custom_user_wallet(sender, instance, created, **kwargs):
    """
    Сигнал для создания нового кошелька будет срабатывать при создании нового пользователя
    """
    if created:
        EmployeeWallet.objects.create(user=instance)
