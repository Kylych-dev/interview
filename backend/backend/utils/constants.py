from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    DIRECTOR = "director", _("Директор")
    TECHNOLOGIST = "technologist", _("Технолог")
    OTK = "otk", _("ОТК")
    SEAMSTRESS = "seamstress", _("Швея")
    IRON_WORKER = "iron_worker", _("Утюжник")
    BUTTON_ATTACHER = "button_attacher", _("Пуговщик")
    PACKER = "packer", _("Упаковщик")
    WAREHOUSEMAN = "Warehouseman", _("Складовщик")
    CUTTER = "Cutter", _("Кройщик")


class SocialNetworkChoices(models.TextChoices):
    FACEBOOK = "Facebook", _("Facebook")
    TWITTER = "Twitter", _("Twitter")
    INSTAGRAM = "Instagram", _("Instagram")
    LINKEDIN = "LinkedIn", _("LinkedIn")
    WHATSAPP = "Whatsapp", _("Whatsapp")
    TELEGRAM = "TELEGRAM", _("Telegram")
    OTHER = "Other", _("Other")


class Status(models.TextChoices):
    IN_PROGRESS = "in_progress", _("В работе")
    IN_CHECK = "in_check", _("На проверке")
    COMPLETED = "completed", _("Сделано")


class OrderStatus(models.TextChoices):
    START = "start", _("В обработке")
    WAREHOUSE = "warehouse", _("Подготовка сырья")
    CUTTING = "cutting", _("Крой")
    PRODUCTION = "production", _("В Производство")
    READY = "ready", _("Готово к отправке")
    COMPLETED = "completed", _("Выполнено")


class SizeChoices(models.IntegerChoices):
    SIZE_42 = 42, _("42")
    SIZE_44 = 44, _("44")
    SIZE_46 = 46, _("46")
    SIZE_48 = 48, _("48")
    SIZE_50 = 50, _("50")
    SIZE_52 = 52, _("52")
    SIZE_54 = 54, _("54")
    SIZE_56 = 56, _("56")
    SIZE_58 = 58, _("58")
    SIZE_60 = 60, _("60")
    SIZE_62 = 62, _("62")
    SIZE_64 = 64, _("64")
    SIZE_66 = 66, _("66")
    SIZE_68 = 68, _("68")
    SIZE_70 = 70, _("70")


class UnitChoices(models.TextChoices):
    PIECE = "шт", _("Штук")
    METER = "метр", _("Метр")
    KILOGRAM = "кг", _("Килограмм")
    ROLL = "рулон", _("Рулон")
    PACK = "пачка", _("Пачка")
    LITER = "литр", _("Литр")
    SQUARE_METER = "м²", _("Квадратный метр")
    CUBIC_METER = "м³", _("Кубический метр")
    GRAM = "грамм", _("Грамм")
    MILLIMETER = "мм", _("Миллиметр")
    CENTIMETER = "см", _("Сантиметр")
    BOTTLE = "бутылка", _("Бутылка")
    SET = "набор", _("Набор")
    PAIR = "пара", _("Пара")
    BOX = "коробка", _("Коробка")
    PACKAGE = "упаковка", _("Упаковка")
    BAG = "мешок", _("Мешок")
    CASE = "ящик", _("Ящик")


class ProductStatus(models.TextChoices):
    SEAMSTRESS = "seamstress", _("Швея")
    TECHNOLOGIST = "technologist", _("Технолог")
    OTK = "otk", _("ОТК")
    IRON_WORKER = "iron_worker", _("Утюжник")
    PACKER = "packer", _("Упаковщик")
    COMPLETED = "completed", _("Выполнено")
