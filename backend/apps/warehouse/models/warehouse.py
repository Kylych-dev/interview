from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.warehouse.models.material import MaterialTemplate
from apps.workshop.models import SewingWorkshop


class Warehouse(models.Model):
    """
    Модель для представления склада швейного цеха.
    Логика заказов:

    Создание заказа: Метод для создания нового заказа, который может включать в себя выбор товаров, количество и т.д.
    Отмена заказа: Возможность отмены заказа до его выполнения.
    Отслеживание статуса заказа: Методы для отслеживания статуса заказа, например, "в обработке", "выполнен", "доставлен" и т.д.
    Логика поставок:

    Запрос цены и наличия: Метод для запроса у поставщика цен и наличия товаров.
    Получение поставок: Запись поступления товаров от поставщиков на склад.
    Уведомления о поставках: Уведомление заинтересованных сторон (например, отдела закупок) о поступлении товаров.
    Логика продуктов:

    Добавление новых продуктов: Метод для добавления новых продуктов на склад.
    Управление ассортиментом: Методы для изменения ассортимента товаров на складе.
    Логика отчетности:

    Генерация отчетов: Создание отчетов о текущем состоянии склада, истории поставок, выполненных заказах и т.д.
    Мониторинг и аналитика: Системы мониторинга и аналитики для отслеживания эффективности работы склада.
    Логика безопасности:

    Управление доступом: Ограничение доступа к различным функциям склада в зависимости от ролей пользователя.
    Журналирование действий: Запись действий пользователей для последующего аудита.
    Логика оповещений:

    Уведомления о низких запасах: Автоматические уведомления при достижении определенного уровня запасов.
    Уведомления о событиях: Оповещения о важных событиях, таких как поступление крупной партии товаров или задержка поставок.
    """

    sewing_workshop = models.OneToOneField(
        SewingWorkshop,
        on_delete=models.PROTECT,
        related_name="warehouse",
        verbose_name=_("Цех"),
    )
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)
    # supply_history = models.ManyToManyField(Supply)  # Подставьте свою модель для истории поставок
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Склад - {self.sewing_workshop.name}"

    def get_inventory_material(self):
        """
        Получить информацию о количестве сырья на складе.
        Возвращает словарь, где ключ - это имя материала/продукции, а значение - количество.
        """
        inventory = {}

        # Получаем все сырье на складе
        raw_materials = WarehouseMaterial.objects.filter(warehouse=self)
        for material in raw_materials:
            inventory[material.raw_material.name] = material.quantity

        return inventory

    def get_inventory_product(self):
        """
        Получить информацию о количестве продукции на складе.
        Возвращает словарь, где ключ - это имя материала/продукции, а значение - количество.
        """
        inventory = {}

        # Получаем все продукты на складе
        products = self.products.filter(is_active=True)

        for product in products:
            inventory[product.name] = product.warehousematerial.quantity

        return inventory

    def add_finished_goods(self, product, quantity):
        # Логика для добавления готового товара на склад
        pass

    def create_product_from_raw_materials(self, product, raw_materials):
        # Логика для создания товара из сырья на складе
        pass

    def record_cut_creation(self, cut_name, raw_materials):
        """
        Record the creation of a cut from raw materials.
        """
        # Assuming cut_name is a string representing the name of the cut

        # Record consumption of raw materials
        # for raw_material, quantity in raw_materials.items():
        #     self.record_raw_material_consumption(raw_material, quantity)
        #
        # # Create the cut (assuming Cut is a model in your backend)
        # cut = Cut.objects.create(
        #     name=cut_name,
        #     warehouse=self
        # )
        #
        # return cut

    def record_raw_material_receipt(self, raw_material, quantity):
        # Запись информации о поступлении сырья на склад
        pass

    def record_raw_material_consumption(self, raw_material, quantity):
        # Запись информации о расходе сырья со склада

        MaterialIncome.objects.create(
            material=self,
            quantity=quantity,
            action_type="outcome",
            cost=raw_material.unit_price,
        )

    def record_production(self, product, quantity):
        # Запись информации о производстве готового товара
        pass

    def record_product_shipment(self, product, quantity):
        # Запись информации о отправке готового товара со склада
        pass

    def add_items(self, product, quantity):
        # Логика для добавления товаров на склад
        pass

    def remove_items(self, product, quantity):
        # Логика для списания товаров со склада
        pass

    def record_supply(self, supplier, product, quantity):
        # Запись информации о поставке на склад
        pass

    def get_supply_history(self):
        # Получение истории поставок
        pass

    def reserve_items(self, order, product, quantity):
        # Логика для резервирования товаров для заказа
        pass

    def fulfill_order(self, order):
        # Логика для подтверждения выполнения заказа и списания товаров со склада
        pass

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        db_table = "sewing_warehouse"


class WarehouseMaterial(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name="Склад",
        related_name="warehouse_material",
        on_delete=models.CASCADE,
    )
    material = models.ForeignKey(
        MaterialTemplate,
        verbose_name="Сырье",
        related_name="warehouse_material",
        on_delete=models.DO_NOTHING,
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name=_("Количество / Метр / Вес")
    )
    is_delete = models.BooleanField(default=False, verbose_name=_("Удаленно"))

    def __str__(self):
        return f"{self.material.name}"

    class Meta:
        verbose_name = _("2. Сырье на складе")
        verbose_name_plural = _("2. Сырье на складе")

    def get_history(self):
        return MaterialIncome.objects.filter(material=self).order_by("-timestamp")


class MaterialIncome(models.Model):
    material = models.ForeignKey(
        WarehouseMaterial, on_delete=models.CASCADE, verbose_name=_("Сырье")
    )
    # todo добавить сумму последней ценый, чтобы сравнивать ее с кол-вом
    quantity = models.PositiveIntegerField(default=0, verbose_name=_("Количество"))
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Стоимость"),
        help_text="Стоимость за ед.",
    )
    is_delete = models.BooleanField(verbose_name=_("Удалено"), default=False)
    timestamp = models.DateTimeField(
        default=timezone.now, verbose_name=_("Дата поступления")
    )

    def __str__(self):
        return f"{self.material.material.name} - {self.quantity} {self.material.material.unit}. ({self.timestamp})"

    class Meta:
        verbose_name = _("История прихода")
        verbose_name_plural = _("История прихода")


class MaterialCutOutcome(models.Model):
    cut = models.ForeignKey("cut.Cut", on_delete=models.DO_NOTHING)
    is_ready = models.BooleanField("Сырье отправлено кройщику", default=False)

    def __str__(self):
        return f"Расход сырья на крой для заказа: {self.cut.order.name}"

    class Meta:
        verbose_name = _("2.1 Расход сырья на крой")
        verbose_name_plural = _("2.1 Расход сырья на крой")


class MaterialFabricationOutcome(models.Model):
    fabric = models.ForeignKey("fabrication.Fabrication", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Расход сырья на производство для заказа: {self.fabric.order.name}"

    class Meta:
        verbose_name = _("4.1 Расход сырья на производство")
        verbose_name_plural = _("4.1 Расход сырья на производство")


class MaterialOutcomeHistory(models.Model):
    material_cut = models.ForeignKey(
        MaterialCutOutcome,
        on_delete=models.CASCADE,
        related_name="outcome_history",
        verbose_name=_("расход на крой"),
        help_text="Заполнятеся когда пишется расход на производство",
        null=True,
        blank=True,
    )
    material_fabric = models.ForeignKey(
        MaterialFabricationOutcome,
        on_delete=models.CASCADE,
        related_name="outcome_history",
        verbose_name=_("расход на производство"),
        help_text="Заполнятеся когда пишется расход на производство",
        null=True,
        blank=True,
    )
    material = models.ForeignKey(
        WarehouseMaterial,
        on_delete=models.CASCADE,
        verbose_name=_("Сырье"),
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name=_("Количество"))
    timestamp = models.DateTimeField(
        default=timezone.now, verbose_name=_("Дата расхода")
    )

    def __str__(self):
        return f"{self.material.material.name} - {self.quantity} {self.material.material.unit}. ({self.timestamp})"

    class Meta:
        verbose_name = _("История расхода")
        verbose_name_plural = _("История расхода")
