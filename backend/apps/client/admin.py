# your_app/admin.py
from django.contrib import admin
from .models import SocialNetworks, Client


class SocialNetworksInline(admin.TabularInline):
    model = SocialNetworks
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'address',)
    search_fields = ('full_name', 'phone_number')
    list_filter = ('social_network',)
    inlines = (SocialNetworksInline,)