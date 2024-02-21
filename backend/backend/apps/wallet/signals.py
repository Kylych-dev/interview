from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.wallet.models import Transaction


@receiver(post_save, sender=Transaction)
def add_amount_wallet_balance(sender, instance, created, **kwargs):
    """
    Сигнал для добавления суммы в кошельке
    """
    if not created:
        # Если транзакция не новая, то не обновляем баланс
        return

    if instance.amount < 0:
        # Если сумма транзакции отрицательная, то не обновляем баланс
        return

    if instance.is_advance:
        # Если запрос на аванс то ничего не делаем
        return

    wallet = instance.wallet
    wallet.balance += instance.amount
    wallet.save()
