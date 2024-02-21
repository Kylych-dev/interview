from django.apps import AppConfig


class FabricationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.fabrication"

    def ready(self):
        import apps.fabrication.signals
