from django.apps import AppConfig


class WorkshopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.workshop"
    verbose_name = "Щвейные цеха"

    def ready(self):
        import apps.workshop.signals
