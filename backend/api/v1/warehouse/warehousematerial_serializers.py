from rest_framework import serializers
from apps.warehouse.models.warehouse import WarehouseMaterial
from apps.warehouse.models.material import MaterialTemplate
from api.v1.warehouse.material_template_serializers import MaterialTemplateSerializer


class WarehouseMaterialSerializer(serializers.ModelSerializer):
    material = MaterialTemplateSerializer()

    class Meta:
        model = WarehouseMaterial
        fields = (
            "material",
            "quantity",
        )
