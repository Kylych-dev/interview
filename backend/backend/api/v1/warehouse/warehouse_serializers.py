from rest_framework import serializers
from apps.warehouse.models.warehouse import Warehouse
from .serializers import ProductCategory, ProductSerializer

class WarehouseSerializer(serializers.ModelSerializer):
    # Подтянуть item serializer
    # items = ItemSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Warehouse
        fields = [
            "id",
            "sewing_workshop",
            # "items",
            "products"
        ]
