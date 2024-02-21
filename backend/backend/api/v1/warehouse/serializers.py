from rest_framework import serializers

from apps.product.models import Product
from apps.order.models import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory     # todo: Кылыч, переделал в ProductCategory, нужно везде удалить ProductTemplate
        fields = [
            "id",
            "name",
            "size",
        ]

# Перенести Product в новый app, product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            # "product_category",
            # "quantity",
            "color",
            "order",
            "color_code",
            "article"
            # "cost",
            # "code",
            # "cut",
            # "photo",
            # "warehouse",
            # "seamstress",
            # "technologist",
            # "iron_worker",
            # "button_attacher",
            # "packer",
            # "otk",
            # "cleaner",
            # "packet",
            # "button",
            # "is_active",
        )


'''
order 
    color 
    
    color_code 
    article 

'''