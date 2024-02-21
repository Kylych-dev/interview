from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils import SocialNetworkChoices
from apps.warehouse.models import Warehouse


class Client(AbstractBaseUser, PermissionsMixin):
    """ Сущность клиента """
    full_name = models.CharField(
        _('ФИО клиента'),
        max_length=300
    )
    email = models.EmailField(
        _('Email клиента'),
        unique=True,
    )
    phone_number = models.CharField(
        _('Номер телефона'),
        max_length=14,
    )
    address = models.CharField(
        _('Адрес'),
        max_length=100,
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="client",
        verbose_name=_("Склад"),
    )
    is_delete = models.BooleanField(
        default=False,
        verbose_name=_('Удален')
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='client_groups',  # Добавь related_name
        related_query_name='client_group',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='client_permissions',  # Добавь related_name
        related_query_name='client_permission',
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    USERNAME_FIELD = 'email' # Используем email для аутентификации
    REQUIRED_FIELDS = ['full_name']  # Добавь сюда обязательные поля для создания пользователя

    def deleted(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    def set_password(self, raw_password='admin1'):
        """
        Устанавливает хешированный пароль для пользователя.
        """
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)
        self.save()

    def __str__(self):
        return f'{self.full_name} - {self.phone_number} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class SocialNetworks(models.Model):
    """ Сущность для социальных сетей """

    name = models.CharField(
        _('Название соц сети'),
        max_length=50,
        choices=SocialNetworkChoices.choices,
        default=SocialNetworkChoices.OTHER,
    )
    link = models.CharField(
        _('Ссылка на соц сеть'),
        max_length=300
    )
    client = models.ForeignKey(
        Client,
        verbose_name='Социальная сеть',
        on_delete=models.DO_NOTHING,
        related_name='social_network',
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'
