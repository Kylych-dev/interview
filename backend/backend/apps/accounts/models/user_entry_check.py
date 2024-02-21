from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser


class UserEntryCheck(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("Сотрудник"),
        null=True, blank=True
    )
    entry_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Время прихода"),
    )
    exit_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Время ухода"),
    )
    is_present = models.BooleanField(
        default=False,
        verbose_name=_("Счётчик явки")
    )
    latitude = models.FloatField(verbose_name=_("Широта"))
    longitude = models.FloatField(verbose_name=_("Долгота"))

    class Meta:
        verbose_name = "Журнал явки сотрудника"
        verbose_name_plural = "Журналы явки сотрудников"

    def __str__(self):
        return (
            f"{self.user.first_name} {self.user.last_name} - {self.entry_time}"
        )
