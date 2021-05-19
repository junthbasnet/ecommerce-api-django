from rest_framework import serializers
from .models import (
    PromoCode,
)


class PromoCodeSerializer(serializers.ModelSerializer):
    """
    Serializes Promocode model instances.
    """
    class Meta:
        model = PromoCode
        fields='__all__'
        read_only_fields = ('created_on', 'modified_on')