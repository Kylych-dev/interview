from rest_framework import serializers
from apps.cut.models import Cut


class CutSerializer(serializers.ModelSerializer):
    """Сериализатор кроя"""

    class Meta:
        model = Cut
        fields = ("order", )
