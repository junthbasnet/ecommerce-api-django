import re
from rest_framework import serializers
from payments.models import PaymentEnvironmentVariable
from .models import PaymentMethod

PAYMENT_METHOD_NAMES = [
    'esewa',
    'fonepay',
    'khalti',
    'imepay',
    'stripe',
    'paypal',
    'cybersource'
]

required_credentials = {
    'esewa': ['ESEWA_SCD'],
    'fonepay': ['FONEPAY_MERCHANT_CODE'],
    'khalti': ['KHALTI_SECRET_KEY'],
    'imepay': ['IME_MERCHANT_CODE', 'IMEPAY_TOKEN', 'IME_MODULE'],
    'stripe': ['STRIPE_API_KEY'],
    'paypal': ['PAYPAL_CLIENT_ID', 'PAYPAL_SECRET'],
    'cybersource': ['CYBERSOURCE_ACCESS_KEY', 'CYBERSOURCE_SECRET_KEY', 'CYBERSOURCE_PROFILE_ID']
}

def get_payment_method_names():
    """
    Returns list of payment method names.
    """
    return PaymentMethod.objects.values_list('method_name', flat=True)


def validate_method_name(method_name):
    """
    Returns True if payment method_name is in PAYMENT_METHOD_NAMES.
    """
    name = method_name.lower()
    if name not in PAYMENT_METHOD_NAMES:
        raise serializers.ValidationError(
                {
                    'method_name': [
                        "Please enter among ['esewa','fonepay','khalti','imepay','stripe','paypal']."
                    ]
                },
                code='invalid_method_name'
            )

    payment_method_names_in_db = [*map(lambda name:name.lower(), get_payment_method_names())]
    if name in payment_method_names_in_db:
        raise serializers.ValidationError(
                {
                    'method_name': [
                        f"{name} already exists."
                    ]
                },
                code='duplicate_name'
            )
    return True


def get_environment_variables_keys():
    """
    Returns list of environment variables keys.
    """
    return PaymentEnvironmentVariable.objects.values_list('key', flat=True)


def is_environment_variables_set(method_name):
    """
    Returns True if environment variables required for payment method is set.
    """
    name = method_name.lower()
    environment_variable_keys = list(get_environment_variables_keys())
    required_keys = required_credentials.get(name)
    is_credentials_set = all([key in environment_variable_keys for key in required_keys])
    if is_credentials_set:
        return True
    else:
        raise serializers.ValidationError(
            {
                'environment_variable': [
                    f"Please set {required_credentials.get(name)} first as environment variable."
                ]
            },
            code='require_environment_variable'
        )







