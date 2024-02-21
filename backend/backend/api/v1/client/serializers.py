from rest_framework import serializers
from apps.client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериализатор Клиента
    """

    class Meta:
        model = Client
        fields = (
            "id",
            "full_name",
            "phone_number",
            "address",
        )
