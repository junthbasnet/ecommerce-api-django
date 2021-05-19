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
    Province,
    City,
    Area,
)
from .utils import (
    validate_method_name,
    is_environment_variables_set,
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
    """
    Serializes payment method model instances.
    """
    class Meta:
        model = PaymentMethod
        fields = (
            'id', 'method_name', 'charge', 'icon', 'priority', 'created_on', 'modified_on',
        )
        read_only_fields = (
            'created_on', 'modified_on',
        )
    
    def validate(self, data):
        """
        Check if payment environment variables are set.
        """

        validate_method_name(data.get('method_name'))
        is_environment_variables_set(data.get('method_name'))
        return data


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        exclude = (
            'modified_on',
            'created_on',
        )


class CitySerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)
    class Meta:
        model = City
        exclude = (
            'modified_on',
            'created_on',
        )


class AreaSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='city.province.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Area
        exclude = (
            'modified_on',
            'created_on',
        )

