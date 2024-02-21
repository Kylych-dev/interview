from django.contrib import admin
from .models import Cut
# from ..product.models import Product


# todo: Кылыч нужно будет удалить отсюда и сделать такой для заказа
# class ProductInline(admin.StackedInline):
#     model = Product
#     extra = 0


@admin.register(Cut)
class CutAdmin(admin.ModelAdmin):
    list_display = ['order', 'created_at']
    search_fields = ['order__id']
    # inlines = (ProductInline,)

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_ready:
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_ready:
            return False

        return True
