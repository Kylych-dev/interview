from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, UserEntryCheck, UserRole


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role", "sewing_workshop")}),)
    #
    # # Добавление поля роли в форму создания пользователя
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (None, {"fields": ("role", "first_name", "last_name", "sewing_workshop")}),
    # )
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "inn",
                    "role",
                    "sewing_workshop"
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "role",
                    "first_name",
                    "last_name",
                    "sewing_workshop",
                    "password1",
                    "password2"
                ),
            },
        ),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("phone_number", "role", "sewing_workshop", "is_superuser", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("phone_number", "first_name", "last_name", "inn")
    ordering = ("phone_number",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


@admin.register(UserEntryCheck)
class EmployeeEntry(admin.ModelAdmin):
    list_display = ('user', 'entry_time', 'exit_time', 'is_present')
    list_filter = ('is_present', 'entry_time')
    search_fields = ('employee__username',)
    date_hierarchy = 'entry_time'
    ordering = ('-entry_time',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass