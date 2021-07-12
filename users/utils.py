from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import serializers
from .models import Shipping


def get_shipping_obj(shipping_id):
    """
    Raises validation error or returns shipping_obj.
    """
    try:
        shipping_obj = Shipping.objects.get(pk=shipping_id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"Shipping with shipping_id:{shipping_id} doesn't exist."
                ]
            },
            code='invalid_shipping_id'
        )
    return shipping_obj