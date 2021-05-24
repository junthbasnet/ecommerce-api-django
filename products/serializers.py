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
    DealOfTheDay,
    PopularPick,
    ProductForPreOrder,
    ProductBundleForPreOrder,
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
    # avg_rating = serializers.CharField(source='average_rating', read_only=True)
    count_of_user_who_rated = serializers.IntegerField(source='count_of_users_who_rated', read_only=True)
    rating_per_stars = serializers.SerializerMethodField(read_only=True)
    is_deal_of_the_day_product = serializers.BooleanField(source='is_deal_of_the_day', read_only=True)
    is_todays_popular_pick_product = serializers.BooleanField(source='is_todays_popular_pick', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = (
            'slug',
        )

    def get_rating_per_stars(self, obj):
        """
        Returns dict of ratings and their respective percentage value.
        """
        rating_count = 1 if obj.reviews.count() == 0 else obj.reviews.count()
        one_star = obj.reviews.filter(rating=1).count() / rating_count * 100 
        two_stars = obj.reviews.filter(rating=2).count() / rating_count * 100 
        three_stars = obj.reviews.filter(rating=3).count() / rating_count * 100 
        four_stars = obj.reviews.filter(rating=4).count() / rating_count * 100 
        five_stars = obj.reviews.filter(rating=5).count() / rating_count * 100 
        return {
            '1':one_star,
            '2':two_stars,
            '3':three_stars,
            '4':four_stars,
            '5':five_stars,
        }


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


class DealOfTheDaySerializer(serializers.ModelSerializer):
    """
    Serializes DealOfTheDay model instances.
    """
    product_data = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = DealOfTheDay
        fields = '__all__'
    
    def get_product_data(self, obj):
        return ProductSerializer(obj.product, context={'request':self.context['request']}).data

class PopularPickSerializer(serializers.ModelSerializer):
    """
    Serializes PopularPick model instances.
    """
    product_data = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PopularPick
        fields = '__all__'
    
    def get_product_data(self, obj):
        return ProductSerializer(obj.product, context={'request':self.context['request']}).data


class ProductForPreOrderSerializer(serializers.ModelSerializer):
    """
    Serializes ProductForPreOrder model instances.
    """
    class Meta:
        model = ProductForPreOrder
        fields = '__all__'


class ProductBundleForPreOrderSerializer(serializers.ModelSerializer):
    """
    Serializes ProductBundleForPreOrder model instances.
    """
    class Meta:
        model=ProductBundleForPreOrder
        fields = '__all__'
        read_only_fields = (
            'slug',
        )







    
