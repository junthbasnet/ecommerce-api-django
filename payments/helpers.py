from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import serializers
from core.models import PaymentMethod
from core.utils import required_credentials
from .models import PaymentEnvironmentVariable


def is_payment_method_obj_in_db(payment_method_name):
    """
    Returns True if object exists with given method name.
    """
    try:
        payment_obj = PaymentMethod.objects.get(slug=payment_method_name)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        return False
    return True


def reverse_required_credentials():
    """
    Returns dict of environment variable to payment method.
    """
    return {value:key for key,values in required_credentials.items() for value in values}


def get_payment_environment_variable_value_for(env_variable_key):
    """
    Returns value of payment environment variable.
    """
    try:
        payment_env_variable_obj = PaymentEnvironmentVariable.objects.get(key=env_variable_key)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        raise serializers.ValidationError(
                {
                    'environment_variable_key': [
                        f"{env_variable_key} doesnt exist."
                    ]
                },
                code='key_not_set'
            )
    return payment_env_variable_obj.value
        

