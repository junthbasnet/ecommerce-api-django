from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from core.models import PaymentMethod
from core.utils import required_credentials


def is_payment_method_obj_in_db(payment_method_name):
    """
    Returns True if object doesn't exist.
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