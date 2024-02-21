from django.db import models
from django.utils.translation import gettext_lazy as _


class MaterialTemplate(models.Model):
    """
    Модель для представления характеристик продукта.
    Вы можете добавить нужные поля, представляющие характеристики продукта.
    """

    name = models.CharField(max_length=255, verbose_name=_("Наименование"))
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Образец Сырья"
        verbose_name_plural = "Образцы Сырья"
