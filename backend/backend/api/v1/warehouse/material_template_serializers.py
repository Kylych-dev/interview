from rest_framework import serializers
from apps.warehouse.models.material import MaterialTemplate


class MaterialTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTemplate
        fields = [
            'id',
            'name',
            # 'unit',
            # 'color',

        ]
