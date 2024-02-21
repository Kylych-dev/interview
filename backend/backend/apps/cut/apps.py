from django.apps import AppConfig


class CutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cut"
    verbose_name = "Крой"

    def ready(self):
        import apps.cut.signals
