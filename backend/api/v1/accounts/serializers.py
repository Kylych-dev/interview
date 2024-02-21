from rest_framework import serializers

from api.v1.sewing_workshop.serializers import SewingWorkshopSerializer
from apps.accounts.models.role_status import UserRole
from apps.accounts.models.models import CustomUser


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = [
            "id",
            "role_name",
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    sewing_workshop = SewingWorkshopSerializer()
    role = UserRoleSerializer()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "profile",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "sewing_workshop",
            "employment_status",
        ]
