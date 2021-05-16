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
        exclude = (
            'modified_on', 'created_on',
        )
        read_only_fields = (
            'slug',
        )


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializes Sub-Category model instances.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = SubCategory
        exclude = (
            'modified_on', 'created_on',
        )
        read_only_fields = (
            'slug', 'category_name',
        )


# class ProductSerializer(serializers.ModelSerializer):
#     """
#     Serializes Product model instances.
#     """
    

    
