from django.contrib import admin

from utils import ProductStatus
from .models import Fabrication, FabricationMoveStatus


class FabricationMoveStatusInline(admin.TabularInline):
    model = FabricationMoveStatus
    extra = 1

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Fabrication)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "created_at", "is_ready")
    search_fields = ("order__name",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    inlines = (FabricationMoveStatusInline,)


@admin.register(FabricationMoveStatus)
class WorkOrderMoveStatusAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        if obj and obj.status == ProductStatus.SEAMSTRESS:
            return False
        return super().has_add_permission(request)
