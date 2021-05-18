import re
from rest_framework import serializers

PAYMENT_METHOD_NAMES = [
    'esewa',
    'fonepay',
    'khalti',
    'imepay',
    'stripe',
    'paypal',
]

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
    return True




