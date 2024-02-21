from django.apps import AppConfig


class WarehouseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.warehouse"
    verbose_name = "Склад"

    def ready(self):
        import apps.warehouse.signals