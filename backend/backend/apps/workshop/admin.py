from django.contrib import admin

from apps.workshop.models import SewingWorkshop


@admin.register(SewingWorkshop)
class SewingWorkshopAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
