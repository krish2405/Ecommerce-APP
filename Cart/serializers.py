from rest_framework import serializers
from .models import CartItems,Cart
from Shop.models import Product
from Shop.serializer import ProductSerializer
class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = CartItems
        fields = ["id", "product", "product_id", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemsSerializer(many=True, read_only=True)
    total_price=serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = Cart
        fields = ["id", "user", "items","total_price"]
        read_only_fields = ["user"]
    
    def get_total_price(self,obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())