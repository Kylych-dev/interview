from django.contrib import admin
from .models import EmployeeWallet, Transaction
from django.utils.translation import gettext_lazy as _


class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(EmployeeWallet)
class EmployeeWalletAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)
    list_display = ("id", "user", "balance")
    search_fields = ("user__username",)
    inlines = (TransactionInline,)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "amount", "date", "description")
    list_filter = ("date",)
    search_fields = ("wallet__user__username", "description")

    def has_change_permission(self, request, obj=None):
        return False
