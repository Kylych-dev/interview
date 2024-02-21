from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.Model):
    role_name = models.CharField(
        verbose_name=_('Название роли'),
        max_length=40,
    )

    def __str__(self):
        return self.role_name


class EmploymentStatus(models.Model):
    status_name = models.CharField(
        verbose_name=_("Название статуса работы"),
        max_length=40,
    )

    def __str__(self):
        return self.status_name
