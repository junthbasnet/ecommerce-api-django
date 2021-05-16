from rest_framework import serializers
from .models import (
    Category,
    SubCategory,
    Product,
    ProductColor,
    ProductImage,
    GlobalSpecification,
)


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes Category model instances.
    """
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'description', 'image', 'priority',
        )
        read_only_fields = (
            'slug',
        )
