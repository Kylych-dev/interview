from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class SewingWorkshop(models.Model):
    """
    Модель для представления швейного цеха.

    Описание:
    Эта модель представляет швейный цех и содержит информацию о нем, такую как название.

    """
    name = models.CharField(
        verbose_name=_('Название цеха'),
        unique=True,
        max_length=100)
    slug = models.SlugField(
        verbose_name=_('Название url'),
        unique=True
    )
    phone_number = models.CharField(
        verbose_name=_('Номер телефона'),
        max_length=15)
    address = models.CharField(
    verbose_name=_("Адрес цеха"), max_length=400)
    latitude = models.FloatField(
        verbose_name=_("Широта"),
        null=True, blank=True
    )
    longitude = models.FloatField(
        verbose_name=_("Долгота"),
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(
        verbose_name=_("Удалено"), 
        default=False
        )

    def get_longitude_latitude(self):
        """
        Метод для получения широты и долготы при помощи адреса цеха
        """
        geo_loc = Nominatim(user_agent='for_test')
        try:
            location = geo_loc.geocode(self.address)
            self.latitude = location.latitude
            self.longitude = location.longitude
        except (GeocoderTimedOut, AttributeError):
            pass

    def update(self, *kwargs):
        """
        Обновление полей объекта с возможным обновлением широты и долготы, если адрес был изменен.
        """
        old_address = self.address
        if 'address' in kwargs:
            self.address = kwargs['address']
        super().save()

        if old_address != self.address:
            self.get_longitude_latitude()
            super().save()

    def save(self, *args, **kwargs):
        if not self.longitude:
            self.get_longitude_latitude()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Швейный цех'
        verbose_name_plural = 'Швейные цеха'
        db_table = 'sewing_workshop'
