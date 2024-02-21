from rest_framework import serializers
from apps.fabrication.models import Fabrication


class FabricationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabrication
        fields = [
            'id',
            'order',
            'is_ready'
        ]

        def create(self, validated_data):
            return Fabrication.objects.create(**validated_data)


