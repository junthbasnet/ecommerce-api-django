from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import (
    Brand,
    Category,
    SubCategory,
    Product,
    ProductImage,
    GlobalSpecification,
    Question,
    Answer,
    RatingAndReview,
)
from users.serializers import UserSerializer


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


class BrandSerializer(serializers.ModelSerializer):
    """
    Serializes Brand model instances.
    """
    class Meta:
        model = Brand
        fields = (
            'id', 'name', 'slug', 'image',
        ) 
        read_only_fields = (
            'slug',
        )


class RatingAndReviewSerializer(serializers.ModelSerializer):
    """
    Serializes rating and review model instances.
    """
    # from orders.serializers import (
    #     OrderProductSerializer,
    # )
    ordered_product_id = serializers.IntegerField(min_value=1, write_only=True)
    # on_ordered_product = OrderProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = RatingAndReview
        fields = (
            'id', 'user', 'product', 'rating', 'review', 'image',
            'ordered_product_id',
        )
        read_only_fields = (
            'user', 'product',
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializes Product model instances.
    """
    category_name = serializers.CharField(source='sub_category.category.name', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = (
            'slug',
        )


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializes ProductImage model instances.
    """
    class Meta:
        model=ProductImage
        fields = (
            'id', 'image',
        )


class GlobalSpecificationSerializer(serializers.ModelSerializer):
    """
    Serializes Global Specification model instances.
    """
    class Meta:
        model = GlobalSpecification
        fields = (
            'id', 'name', 'slug',
        )
        read_only_fields = (
            'slug',
        )


class ProductQuestionSerializer(serializers.ModelSerializer):
    """
    Serializes product questions.
    """
    answer = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    class Meta:
        model = Question
        fields = (
            'id', 'user', 'product', 'question', 'answer', 'is_answered',
            'created_on', 'modified_on',
        )
        read_only_fields = (
            'user', 'created_on', 'modified_on',
            'is_answered', 'answer',
        )
    
    def get_answer(self, obj):
        try:
            return ProductAnswerSerializer(obj.answer).data
        except ObjectDoesNotExist:
            return None


class ProductAnswerSerializer(serializers.ModelSerializer):
    """
    Serializes product questions.
    """
    user = UserSerializer(read_only=True)
    class Meta:
        model = Answer
        fields = (
            'id', 'user', 'question', 'answer',
            'created_on', 'modified_on',
        )
        read_only_fields = (
            'user', 'created_on', 'modified_on',
        )






    
