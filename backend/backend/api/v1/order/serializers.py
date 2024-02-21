from rest_framework import serializers
from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказа"""

    class Meta:
        model = Order
        fields = (
            "client",
            "name",
            "comment",
            "quantity",
            "status",
            "is_done",
            "start_order",
            "end_order",
        )
