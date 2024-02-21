from django.db import models
from django.utils.text import slugify
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.manager import UserManager
from .role_status import UserRole, EmploymentStatus
from apps.accounts.validation import INNValidator, PhoneNumberValidator
from apps.workshop.models import SewingWorkshop


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """

    inn_validator = INNValidator()
    phone_number_validator = PhoneNumberValidator()

    phone_number = models.CharField(
        verbose_name=_("Номер телефона"),
        unique=True,
        max_length=13,
        help_text=_(
            "Обязательное поле. Должно содержать от 10 цифр (0700 123 456) до 12 цифр (+996 700 123 456"
        ),
        validators=[phone_number_validator],
        error_messages={
            "unique": _("Пользователь с таким номером телефона уже существует."),
        },
    )
    slug = models.SlugField(verbose_name=_("Название url"), blank=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    passport_pic = models.ImageField(
        verbose_name=_("Фото пасспорта для верификации"),
        upload_to="passport/pic",
        null=True,
        blank=True,
    )
    profile = models.ImageField(
        upload_to="profile/", null=True, blank=True, verbose_name=_("Profile")
    )
    role = models.ForeignKey(
        UserRole,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Роль пользователя"),
        related_name="user_role",
        null=True, blank=True
    )
    employment_status = models.ForeignKey(
        EmploymentStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Статус работы"),
        related_name="employment_status",
    )
    sewing_workshop = models.ForeignKey(
        SewingWorkshop,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Швейный цех"),
        related_name="sewing_workshop",
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(
        _("verified"),
        default=False,
    )
    verification_code = models.CharField(
        verbose_name=_("verification code"), null=True, blank=True, max_length=6
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    updated_at = models.DateTimeField(_("date updated"), auto_now_add=True)
    inn = models.CharField(
        verbose_name=_("ИНН"),
        max_length=14,
        unique=True,
        null=True,
        blank=True,
        help_text=_("Обязательное поле. Должно содержать 14 цифр"),
        validators=[inn_validator],
        error_messages={
            "unique": _("Пользователь с таким ИНН уже существует."),
        },
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        ordering = ("date_joined",)
        verbose_name = _("user")
        verbose_name_plural = _("users")
        app_label = "accounts"

        constraints = [
            models.UniqueConstraint(
                fields=["phone_number", "inn"],
                name="unique_inn_phone",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_date = self.date_joined.toordinal()
            self.slug = slugify(f"{self.id}{unique_date}{self.date_joined.strftime('%H%M%S%D')}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role.role_name if self.role else ''})"

    def get_phone_number(self):
        return f"+{self.phone_number}"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

