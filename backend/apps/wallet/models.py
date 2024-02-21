from decimal import Decimal

from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _


class EmployeeWallet(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("Сотрудник")
    )
    balance = models.DecimalField(
        verbose_name=_("Баланс"), max_digits=12, decimal_places=2, default=0.00
    )

    def __str__(self):
        return f"Кошелек {self.user.get_full_name()}"

    class Meta:
        verbose_name = _("Кошелек сотрудника")
        verbose_name_plural = _("Кошельки сотрудников")


class Transaction(models.Model):
    wallet = models.ForeignKey(
        EmployeeWallet,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name=_("Кошелек"),
    )
    amount = models.DecimalField(
        verbose_name=_("Сумма"), max_digits=10, decimal_places=2
    )
    date = models.DateTimeField(
        verbose_name=_("Дата транзакции"),
        default=timezone.now(),
        blank=True
    )
    description = models.TextField(verbose_name=_("Описание"))
    is_advance = models.BooleanField(
        verbose_name=_("Запрос на аванс"), default=False
    )

    def __str__(self):
        return (
            f"Транзакция {self.id} на {self.amount} ({self.date.strftime('%Y-%m-%d')})"
        )

    def subtract_wallet_balance(self):
        """
        Вычитает сумму транзакции из баланса кошелька сотрудника. Выплата всей ЗП

        Raises:
            ValidationError: Если сумма транзакции отрицательная или баланс
                кошелька меньше суммы транзакции.
        """
        if self.amount < 0:
            raise ValidationError(_("Сумма транзакции не может быть отрицательной."))

        if self.wallet.balance < self.amount:
            raise ValidationError(_("Не достаточно средств для выдачи наличных."))

        self.wallet.balance -= self.amount
        self.wallet.save()

    def pay_advance(self):
        """
        Выполняет выплату запроса на аванс, увеличивая баланс кошелька сотрудника
        на указанную сумму и помечает транзакцию как выполненную.

        Raises:
            ValidationError: Если транзакция не является запросом на аванс или
                сумма транзакции отрицательная.
        """
        if not self.is_advance:
            raise ValidationError(_("Эта транзакция не является запросом на аванс."))

        if self.amount < 0:
            raise ValidationError(_("Сумма транзакции не может быть отрицательной."))

        self.wallet.balance += self.amount
        self.wallet.save()

        # Помечаем транзакцию как выполненную
        self.is_advance = False
        self.save()

    @classmethod
    def create_advance_request(cls, wallet: EmployeeWallet, amount: Decimal, description: str):
        """
        Создает запрос на аванс и сохраняет его в базе данных.

        Args:
            wallet: Объект кошелька сотрудника, для которого
                создается запрос на аванс.
            amount: Сумма запроса на аванс.
            description: Описание запроса на аванс.

        Returns:
            Transaction: Созданный объект запроса на аванс.

        """
        return cls.objects.create(
            wallet=wallet, amount=amount, description=description, is_advance=True
        )

    class Meta:
        verbose_name = _("Транзакция")
        verbose_name_plural = _("Транзакции")
        ordering = '-id',
