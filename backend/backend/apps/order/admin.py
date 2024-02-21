from django import forms
from django.contrib import admin

from utils import OrderStatus
from .forms import OrderAdminForm
from .models import Order, ProductCategory, Payment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = ('name', 'client', 'status', 'created_at', 'update_at')
    list_filter = ('status', 'created_at', 'update_at')
    search_fields = ('name', 'client__full_name')  # Assuming that 'full_name' is a field in your Client model
    date_hierarchy = 'created_at'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['status'].widget = forms.Select(choices=OrderStatus.choices)
        return form


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
