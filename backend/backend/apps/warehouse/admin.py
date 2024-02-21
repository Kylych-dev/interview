from django.contrib import admin

from apps.warehouse.forms import MaterialOutcomeForm
from apps.warehouse.models import MaterialTemplate
from apps.warehouse.models.warehouse import (
    Warehouse,
    WarehouseMaterial,
    MaterialIncome,
    MaterialOutcomeHistory,
    MaterialCutOutcome,
    MaterialFabricationOutcome,
)


@admin.register(MaterialTemplate)
class MaterialTemplateAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


class WarehouseMaterialInline(admin.TabularInline):
    model = WarehouseMaterial
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    inlines = (WarehouseMaterialInline,)

    def get_inline_instances(self, request, obj=None):
        if obj:
            warehouse_material_inline = WarehouseMaterialInline(
                self.model, self.admin_site
            )
            warehouse_material_inline.queryset = obj.warehouse_material.all()

            return [warehouse_material_inline]
        return []


class MaterialIncomeInline(admin.StackedInline):
    model = MaterialIncome
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WarehouseMaterial)
class WarehouseMaterialAdmin(admin.ModelAdmin):
    list_display = ("warehouse", "material")
    search_fields = ("warehouse__sewing_workshop__name", "material__name")
    readonly_fields = ("quantity",)
    inlines = (MaterialIncomeInline,)


class MaterialOutcomeHistoryInline(admin.StackedInline):
    model = MaterialOutcomeHistory
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MaterialCutOutcome)
class MaterialOutcomeAdmin(admin.ModelAdmin):
    form = MaterialOutcomeForm
    inlines = (MaterialOutcomeHistoryInline,)

    def has_change_permission(self, request, obj=None):
        if obj and obj.cut.is_ready:
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.cut.is_ready:
            return False

        return True


@admin.register(MaterialFabricationOutcome)
class MaterialFabricationOutcomeAdmin(admin.ModelAdmin):
    inlines = (MaterialOutcomeHistoryInline,)

