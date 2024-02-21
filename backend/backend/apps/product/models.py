from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from apps.order.models import Order
from utils import SizeChoices


class Product(models.Model):
    """
    Модель для представления продукции.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Заказ"),
        related_name="products",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Название цвета"),
        max_length=100,
    )
    color_code = models.CharField(
        verbose_name=_("Код цвета"),
        max_length=15,
    )
    article = models.CharField(
        max_length=100, verbose_name=_("Артикул"), null=True, blank=True
    )  # todo: Уточнить по поводу артикула у товара
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)

    def __str__(self):
        return f"Продукт: c заказа {self.order.name}, цвет: {self.color}"

    @transaction.atomic()
    def create_product_sizes(self, sizes, quantity=0):
        """
        Метод для создания объектов ProductSize для данного продукта.

        Аргументы:
        Sizes: list: Список размеров.
        Quantity int: Количество продукции для производства.
        """
        products = []
        for size in sizes:
            products.append(
                ProductSize(
                    product=self,
                    size=size,
                    quantity=quantity,
                )
            )
        ProductSize.objects.bulk_create(products)

    class Meta:
        verbose_name = "Продукция"
        verbose_name_plural = "Продукции"
        db_table = "product"


class ProductSize(models.Model):
    """
    Модель для представления размеров продукции.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Продукт"),
        related_name="sizes",
    )
    size = models.PositiveSmallIntegerField(
        verbose_name=_("Размер"),
        choices=SizeChoices.choices,
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Количество"),
    )

    def __str__(self):
        return f"Размер: {self.get_size_display()}, Количество: {self.quantity}"

    class Meta:
        verbose_name = "Размер продукта"
        verbose_name_plural = "Размеры продуктов"
