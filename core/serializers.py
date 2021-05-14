from rest_framework import serializers

from .models import (
    SiteSetting,
    SEOSetting,
    SocialLinkSetting,
    Slideshow,
    FAQ,
    FAQCategory,
    PaymentMethod,
    Testimonial,
)


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class SEOSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOSetting
        fields = '__all__'


class SocialLinkSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinkSetting
        fields = '__all__'


class SlideshowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slideshow
        fields = '__all__'
        read_only_fields = ('created_on', 'modified_on')


class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = '__all__'
        read_only_fields = ('slug',)


class FAQSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ('slug',)


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        exclude = ('modified_on', 'created_on')
