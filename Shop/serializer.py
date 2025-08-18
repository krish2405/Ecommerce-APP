from rest_framework import serializers
from .models import Category,Product



class ProductSerializer(serializers.ModelSerializer):
    creted_by=serializers.ReadOnlyField(source="created_by.username")
    class Meta:
        model=Product
        fields='__all__'
        read_only_fields = ['created_by']
        extra_kwargs = {
            'created_by': {'required': False}
        }

class CategorySeralizer(serializers.ModelSerializer):
    products=ProductSerializer(many=True,read_only=True)
    class Meta:
        model=Category
        fields='__all__'

