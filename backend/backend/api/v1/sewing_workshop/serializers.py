from rest_framework import serializers
from apps.workshop.models import SewingWorkshop


class SewingWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = SewingWorkshop
        fields = ["id", "name", "phone_number"]
